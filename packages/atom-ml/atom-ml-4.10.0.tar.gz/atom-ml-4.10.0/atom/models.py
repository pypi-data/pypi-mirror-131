# -*- coding: utf-8 -*-

"""
Automated Tool for Optimized Modelling (ATOM)
Author: Mavs
Description: Module containing all available models. All classes must
             have the following structure:

        Name
        ----
        Name of the model's class in camel case format.


        Class attributes
        ----------------
        acronym: str
            Acronym of the model's fullname.

        fullname: str
            Complete name of the model. If None, the estimator's
            __name__ is used.

        needs_scaling: bool
            Whether the model needs scaled features. Can not be
            True for datasets with more than two dimensions.

        goal: str
            If the model is only for classification ("class"),
            regression ("reg") or both ("both").


        Instance attributes
        -------------------
        T: class
            Trainer from which the model is called.

        name: str
            Name of the model. Defaults to the same as the acronym
            but can be different if the same model is called multiple
            times. The name is assigned in the basemodel.py module.

        evals: dict
            Evaluation metric and scores. Only for models that allow
            in-train evaluation.

        params: dict
            All the estimator's parameters for the BO. The values
            should be a list with two elements, the parameter's
            default value and the number of decimals.


        Properties
        ----------
        est_class: estimator's base class
            Base class (not instance) of the underlying estimator.


        Methods
        -------
        __init__(self, *args):
            Class initializer. Contains super() to the BaseModel class.

        get_init_values(self):
            Return the initial values for the estimator. Don't implement
            if the method in BaseModel (default behaviour) is sufficient.

        get_params(self, x):
            Return the parameters with rounded decimals and (optional)
            custom changes to the params. Don't implement if the method
            in BaseModel (default behaviour) is sufficient.

        get_estimator(self, params=None):
            Return the model's estimator with unpacked parameters.

        custom_fit(model, train, validation, est_params):
            This method is called instead of directly running the
            estimator's fit method. Implement only to customize the fit.

        get_dimensions(self):
            Return a list of the bounds for the hyperparameters.


To add a new model:
    1. Add the model's class to models.py
    2. Add the model to the list MODELS in models.py


List of available models:
    - "Dummy" for Dummy Classifier/Regressor
    - "GNB" for Gaussian Naive Bayes (no hyperparameter tuning)
    - "MNB" for Multinomial Naive Bayes
    - "BNB" for Bernoulli Naive Bayes
    - "CatNB" for Categorical Naive Bayes
    - "CNB" for Complement Naive Bayes
    - "GP" for Gaussian Process (no hyperparameter tuning)
    - "OLS" for Ordinary Least Squares (no hyperparameter tuning)
    - "Ridge" for Ridge Linear Classifier/Regressor
    - "Lasso" for Lasso Linear Regression
    - "EN" for ElasticNet Linear Regression
    - "BR" for Bayesian Ridge
    - "ARD" for Automated Relevance Determination
    - "LR" for Logistic Regression
    - "LDA" for Linear Discriminant Analysis
    - "QDA" for Quadratic Discriminant Analysis
    - "KNN" for K-Nearest Neighbors
    - "RNN" for Radius Nearest Neighbors
    - "Tree" for a single Decision Tree
    - "Bag" for Bagging
    - "ET" for Extra-Trees
    - "RF" for Random Forest
    - "AdaB" for AdaBoost
    - "GBM" for Gradient Boosting Machine
    - "hGBM" for Hist Gradient Boosting Machine
    - "XGB" for XGBoost (if package is available)
    - "LGB" for LightGBM (if package is available)
    - "CatB" for CatBoost (if package is available)
    - "lSVM" for Linear Support Vector Machine
    - "kSVM" for Kernel (non-linear) Support Vector Machine
    - "PA" for Passive Aggressive
    - "SGD" for Stochastic Gradient Descent
    - "MLP" for Multi-layer Perceptron

Additionally, ATOM implements two ensemble models:
    - "Stack" for Stacking
    - "Vote" for Voting

"""

# Standard packages
import numpy as np
from copy import copy
from random import randint
from inspect import signature
from scipy.spatial.distance import cdist
from skopt.space.space import Real, Integer, Categorical

# Sklearn estimators
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.gaussian_process import (
    GaussianProcessClassifier,
    GaussianProcessRegressor
)
from sklearn.naive_bayes import (
    GaussianNB,
    MultinomialNB,
    BernoulliNB,
    CategoricalNB,
    ComplementNB,
)
from sklearn.linear_model import (
    LinearRegression,
    RidgeClassifier,
    Ridge as RidgeRegressor,
    Lasso as LassoRegressor,
    ElasticNet as ElasticNetRegressor,
    BayesianRidge as BayesianRidgeRegressor,
    ARDRegression,
    LogisticRegression as LR,
)
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis as LDA,
    QuadraticDiscriminantAnalysis as QDA,
)
from sklearn.neighbors import (
    KNeighborsClassifier,
    KNeighborsRegressor,
    RadiusNeighborsClassifier,
    RadiusNeighborsRegressor,
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    BaggingClassifier,
    BaggingRegressor,
    ExtraTreesClassifier,
    ExtraTreesRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
    AdaBoostClassifier,
    AdaBoostRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
)
from sklearn.svm import LinearSVC, LinearSVR, SVC, SVR
from sklearn.linear_model import (
    PassiveAggressiveClassifier,
    PassiveAggressiveRegressor,
    SGDClassifier,
    SGDRegressor,
)
from sklearn.neural_network import MLPClassifier, MLPRegressor

# Own modules
from .basemodel import BaseModel
from .pipeline import Pipeline
from .ensembles import (
    VotingClassifier,
    VotingRegressor,
    StackingClassifier,
    StackingRegressor,
)
from .utils import create_acronym, CustomDict


class CustomModel(BaseModel):
    """Custom model. Estimator provided by user."""

    def __init__(self, *args, **kwargs):
        self.est = kwargs["estimator"]  # Estimator provided by the user

        # If no fullname is provided, use the class' name
        if hasattr(self.est, "fullname"):
            self.fullname = self.est.fullname
        elif callable(self.est):
            self.fullname = self.est.__name__
        else:
            self.fullname = self.est.__class__.__name__

        # If no acronym is provided, use capital letters in the class' name
        if hasattr(self.est, "acronym"):
            self.acronym = self.est.acronym
        else:
            self.acronym = create_acronym(self.fullname)

        self.needs_scaling = getattr(self.est, "needs_scaling", False)
        super().__init__(*args)

    @property
    def est_class(self):
        """Return the estimator's class."""
        if callable(self.est):
            return self.est
        else:
            return self.est.__class__

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        sign = signature(self.est.__init__).parameters

        # The provided estimator can be a class or an instance
        if callable(self.est):
            # Add n_jobs and random_state to the estimator (if available)
            for p in ("n_jobs", "random_state"):
                if p in sign:
                    params[p] = params.pop(p, getattr(self.T, p))

            return self.est(**params)

        else:
            # Update the parameters (only if it's a BaseEstimator)
            if all(hasattr(self.est, attr) for attr in ("get_params", "set_params")):
                for p in ("n_jobs", "random_state"):
                    # If the class has the parameter and it's the default value
                    if p in sign and self.est.get_params()[p] == sign[p]._default:
                        params[p] = params.pop(p, getattr(self.T, p))

                self.est.set_params(**params)

            return self.est


class Dummy(BaseModel):
    """Dummy classifier/regressor."""

    acronym = "Dummy"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)

        if self.T.goal == "class":
            self.fullname = "Dummy Classification"
            self.params = {"strategy": ["prior", 0]}
        else:
            self.fullname = "Dummy Regression"
            self.params = {"strategy": ["mean", 0], "quantile": [0.5, 2]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return DummyClassifier
        else:
            return DummyRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        if self.T.goal == "class":
            return self.est_class(
                random_state=params.pop("random_state", self.T.random_state),
                **params,
            )
        else:
            return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        if self.T.goal == "class":
            strategies = ["stratified", "most_frequent", "prior", "uniform"]
            dimensions = [Categorical(strategies, name="strategy")]
        else:
            dimensions = [
                Categorical(["mean", "median", "quantile"], name="strategy"),
                Real(0.0, 1.0, name="quantile"),
            ]
        return [d for d in dimensions if d.name in self.params]


class GaussianProcess(BaseModel):
    """Gaussian process."""

    acronym = "GP"
    fullname = "Gaussian Process"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return GaussianProcessClassifier
        else:
            return GaussianProcessRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        if self.T.goal == "class":
            return self.est_class(
                random_state=params.pop("random_state", self.T.random_state),
                n_jobs=params.pop("n_jobs", self.T.n_jobs),
                **params,
            )
        else:
            return self.est_class(
                random_state=params.pop("random_state", self.T.random_state),
                **params,
            )


class GaussianNaiveBayes(BaseModel):
    """Gaussian Naive Bayes."""

    acronym = "GNB"
    fullname = "Gaussian Naive Bayes"
    needs_scaling = False
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def est_class(self):
        """Return the estimator's class."""
        return GaussianNB

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)


class MultinomialNaiveBayes(BaseModel):
    """Multinomial Naive Bayes."""

    acronym = "MNB"
    fullname = "Multinomial Naive Bayes"
    needs_scaling = False
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"alpha": [1.0, 3], "fit_prior": [True, 0]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        return MultinomialNB

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Real(1e-3, 10, "log-uniform", name="alpha"),
            Categorical([True, False], name="fit_prior"),
        ]
        return [d for d in dimensions if d.name in self.params]


class BernoulliNaiveBayes(BaseModel):
    """Bernoulli Naive Bayes."""

    acronym = "BNB"
    fullname = "Bernoulli Naive Bayes"
    needs_scaling = False
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"alpha": [1.0, 3], "fit_prior": [True, 0]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        return BernoulliNB

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Real(1e-3, 10, "log-uniform", name="alpha"),
            Categorical([True, False], name="fit_prior"),
        ]
        return [d for d in dimensions if d.name in self.params]


class CategoricalNaiveBayes(BaseModel):
    """Categorical Naive Bayes."""

    acronym = "CatNB"
    fullname = "Categorical Naive Bayes"
    needs_scaling = False
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"alpha": [1.0, 3], "fit_prior": [True, 0]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        return CategoricalNB

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Real(1e-3, 10, "log-uniform", name="alpha"),
            Categorical([True, False], name="fit_prior"),
        ]
        return [d for d in dimensions if d.name in self.params]


class ComplementNaiveBayes(BaseModel):
    """Complement Naive Bayes."""

    acronym = "CNB"
    fullname = "Complement Naive Bayes"
    needs_scaling = False
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"alpha": [1.0, 3], "fit_prior": [True, 0], "norm": [False, 0]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        return ComplementNB

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Real(1e-3, 10, "log-uniform", name="alpha"),
            Categorical([True, False], name="fit_prior"),
            Categorical([True, False], name="norm"),
        ]
        return [d for d in dimensions if d.name in self.params]


class OrdinaryLeastSquares(BaseModel):
    """Linear Regression (without regularization)."""

    acronym = "OLS"
    fullname = "Ordinary Least Squares"
    needs_scaling = True
    goal = "reg"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def est_class(self):
        """Return the estimator's class."""
        return LinearRegression

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(n_jobs=params.pop("n_jobs", self.T.n_jobs), **params)


class Ridge(BaseModel):
    """Linear Regression/Classification with ridge regularization."""

    acronym = "Ridge"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"alpha": [1.0, 3], "solver": ["auto", 0]}

        if self.T.goal == "class":
            self.fullname = "Ridge Classification"
        else:
            self.fullname = "Ridge Regression"

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return RidgeClassifier
        else:
            return RidgeRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        solvers = ["auto", "svd", "cholesky", "lsqr", "sparse_cg", "sag", "saga"]
        dimensions = [
            Real(1e-3, 10, "log-uniform", name="alpha"),
            Categorical(solvers, name="solver"),
        ]
        return [d for d in dimensions if d.name in self.params]


class Lasso(BaseModel):
    """Linear Regression with lasso regularization."""

    acronym = "Lasso"
    fullname = "Lasso Regression"
    needs_scaling = True
    goal = "reg"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"alpha": [1.0, 3], "selection": ["cyclic", 0]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        return LassoRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Real(1e-3, 10, "log-uniform", name="alpha"),
            Categorical(["cyclic", "random"], name="selection"),
        ]
        return [d for d in dimensions if d.name in self.params]


class ElasticNet(BaseModel):
    """Linear Regression with elasticnet regularization."""

    acronym = "EN"
    fullname = "ElasticNet Regression"
    needs_scaling = True
    goal = "reg"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "alpha": [1.0, 3],
            "l1_ratio": [0.5, 1],
            "selection": ["cyclic", 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        return ElasticNetRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Real(1e-3, 10, "log-uniform", name="alpha"),
            Categorical(np.linspace(0.1, 0.9, 9), name="l1_ratio"),
            Categorical(["cyclic", "random"], name="selection"),
        ]
        return [d for d in dimensions if d.name in self.params]


class BayesianRidge(BaseModel):
    """Bayesian ridge regression."""

    acronym = "BR"
    fullname = "Bayesian Ridge"
    needs_scaling = True
    goal = "reg"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "n_iter": [300, 0],
            "alpha_1": [1e-6, 8],
            "alpha_2": [1e-6, 8],
            "lambda_1": [1e-6, 8],
            "lambda_2": [1e-6, 8],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        return BayesianRidgeRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(100, 1000, name="n_iter"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="alpha_1"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="alpha_2"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="lambda_1"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="lambda_2"),
        ]
        return [d for d in dimensions if d.name in self.params]


class AutomaticRelevanceDetermination(BaseModel):
    """Automatic Relevance Determination."""

    acronym = "ARD"
    fullname = "Automatic Relevant Determination"
    needs_scaling = True
    goal = "reg"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "n_iter": [300, 0],
            "alpha_1": [1e-6, 8],
            "alpha_2": [1e-6, 8],
            "lambda_1": [1e-6, 8],
            "lambda_2": [1e-6, 8],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        return ARDRegression

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(100, 1000, name="n_iter"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="alpha_1"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="alpha_2"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="lambda_1"),
            Categorical([1e-8, 1e-6, 1e-4, 1e-2], name="lambda_2"),
        ]
        return [d for d in dimensions if d.name in self.params]


class LogisticRegression(BaseModel):
    """Logistic Regression."""

    acronym = "LR"
    fullname = "Logistic Regression"
    needs_scaling = True
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "penalty": ["l2", 0],
            "C": [1.0, 3],
            "solver": ["lbfgs", 0],
            "max_iter": [100, 0],
            "l1_ratio": [0.5, 1],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        return LR

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        # Limitations on penalty + solver combinations
        penalty, solver = params.get("penalty"), params.get("solver")
        cond_1 = penalty == "none" and solver == "liblinear"
        cond_2 = penalty == "l1" and solver not in ("liblinear", "saga")
        cond_3 = penalty == "elasticnet" and solver != "saga"

        if cond_1 or cond_2 or cond_3:
            params["penalty"] = "l2"  # Change to default value

        if params.get("penalty") != "elasticnet":
            params.pop("l1_ratio")
        if params.get("penalty") == "none":
            params.pop("C")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        solvers = ["lbfgs", "newton-cg", "liblinear", "sag", "saga"]
        dimensions = [
            Categorical(["none", "l1", "l2", "elasticnet"], name="penalty"),
            Real(1e-3, 100, "log-uniform", name="C"),
            Categorical(solvers, name="solver"),
            Integer(100, 1000, name="max_iter"),
            Categorical(np.linspace(0.1, 0.9, 9), name="l1_ratio"),
        ]
        return [d for d in dimensions if d.name in self.params]


class LinearDiscriminantAnalysis(BaseModel):
    """Linear Discriminant Analysis."""

    acronym = "LDA"
    fullname = "Linear Discriminant Analysis"
    needs_scaling = False
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"solver": ["svd", 0], "shrinkage": [0, 1]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        return LDA

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        if params.get("solver") == "svd":
            params.pop("shrinkage")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Categorical(["svd", "lsqr", "eigen"], name="solver"),
            Categorical(np.linspace(0.0, 1.0, 11), name="shrinkage"),
        ]
        return [d for d in dimensions if d.name in self.params]


class QuadraticDiscriminantAnalysis(BaseModel):
    """Quadratic Discriminant Analysis."""

    acronym = "QDA"
    fullname = "Quadratic Discriminant Analysis"
    needs_scaling = False
    goal = "class"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"reg_param": [0, 1]}

    @property
    def est_class(self):
        """Return the estimator's class."""
        return QDA

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [Categorical(np.linspace(0.0, 1.0, 11), name="reg_param")]
        return [d for d in dimensions if d.name in self.params]


class KNearestNeighbors(BaseModel):
    """K-Nearest Neighbors."""

    acronym = "KNN"
    fullname = "K-Nearest Neighbors"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "n_neighbors": [5, 0],
            "weights": ["uniform", 0],
            "algorithm": ["auto", 0],
            "leaf_size": [30, 0],
            "p": [2, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return KNeighborsClassifier
        else:
            return KNeighborsRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(1, 100, name="n_neighbors"),
            Categorical(["uniform", "distance"], name="weights"),
            Categorical(["auto", "ball_tree", "kd_tree", "brute"], name="algorithm"),
            Integer(20, 40, name="leaf_size"),
            Integer(1, 2, name="p"),
        ]
        return [d for d in dimensions if d.name in self.params]


class RadiusNearestNeighbors(BaseModel):
    """Radius Nearest Neighbors."""

    acronym = "RNN"
    fullname = "Radius Nearest Neighbors"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        self._distances = None
        super().__init__(*args)
        self.params = {
            "radius": [None, 3],  # The scaler is needed to calculate the distances
            "weights": ["uniform", 0],
            "algorithm": ["auto", 0],
            "leaf_size": [30, 0],
            "p": [2, 0],
        }

    @property
    def distances(self):
        """Return distances between a random subsample of rows."""
        if self._distances is None:
            self._distances = cdist(
                self.X_train.select_dtypes("number").sample(50),
                self.X_train.select_dtypes("number").sample(50),
            ).flatten()

        return self._distances

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return RadiusNeighborsClassifier
        else:
            return RadiusNeighborsRegressor

    def get_init_values(self):
        """Custom method to return a valid radius."""
        return [np.mean(self.distances)] + super().get_init_values()[1:]

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        if self.T.goal == "class":
            return self.est_class(
                outlier_label=params.pop("outlier_label", "most_frequent"),
                radius=params.pop("radius", np.mean(self.distances)),
                n_jobs=params.pop("n_jobs", self.T.n_jobs),
                **params,
            )
        else:
            return self.est_class(
                radius=params.pop("radius", np.mean(self.distances)),
                n_jobs=params.pop("n_jobs", self.T.n_jobs),
                **params,
            )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        algorithms = ["auto", "ball_tree", "kd_tree", "brute"]

        dimensions = [
            Real(min(self.distances), max(self.distances), name="radius"),
            Categorical(["uniform", "distance"], name="weights"),
            Categorical(algorithms, name="algorithm"),
            Integer(20, 40, name="leaf_size"),
            Integer(1, 2, name="p"),
        ]
        return [d for d in dimensions if d.name in self.params]


class DecisionTree(BaseModel):
    """Single Decision Tree."""

    acronym = "Tree"
    fullname = "Decision Tree"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "criterion": ["gini" if self.T.goal == "class" else "squared_error", 0],
            "splitter": ["best", 0],
            "max_depth": [None, 0],
            "min_samples_split": [2, 0],
            "min_samples_leaf": [1, 0],
            "max_features": [None, 0],
            "ccp_alpha": [0, 3],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return DecisionTreeClassifier
        else:
            return DecisionTreeRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        if self.T.goal == "class":
            criterion = ["gini", "entropy"]
        else:
            criterion = ["squared_error", "absolute_error", "friedman_mse", "poisson"]

        dimensions = [
            Categorical(criterion, name="criterion"),
            Categorical(["best", "random"], name="splitter"),
            Categorical([None, *list(range(1, 10))], name="max_depth"),
            Integer(2, 20, name="min_samples_split"),
            Integer(1, 20, name="min_samples_leaf"),
            Categorical([None, *np.linspace(0.5, 0.9, 5)], name="max_features"),
            Real(0, 0.035, name="ccp_alpha"),
        ]
        return [d for d in dimensions if d.name in self.params]


class Bagging(BaseModel):
    """Bagging model (with decision tree as base estimator)."""

    acronym = "Bag"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "n_estimators": [10, 0],
            "max_samples": [1.0, 1],
            "max_features": [1.0, 1],
            "bootstrap": [True, 0],
            "bootstrap_features": [False, 0],
        }

        if self.T.goal == "class":
            self.fullname = "Bagging Classifier"
        else:
            self.fullname = "Bagging Regressor"

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return BaggingClassifier
        else:
            return BaggingRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(10, 500, name="n_estimators"),
            Categorical(np.linspace(0.5, 1.0, 6), name="max_samples"),
            Categorical(np.linspace(0.5, 1.0, 6), name="max_features"),
            Categorical([True, False], name="bootstrap"),
            Categorical([True, False], name="bootstrap_features"),
        ]
        return [d for d in dimensions if d.name in self.params]


class ExtraTrees(BaseModel):
    """Extremely Randomized Trees."""

    acronym = "ET"
    fullname = "Extra-Trees"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "n_estimators": [100, 0],
            "criterion": ["gini" if self.T.goal == "class" else "squared_error", 0],
            "max_depth": [None, 0],
            "min_samples_split": [2, 0],
            "min_samples_leaf": [1, 0],
            "max_features": [None, 0],
            "bootstrap": [False, 0],
            "ccp_alpha": [0, 3],
            "max_samples": [0.9, 1],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return ExtraTreesClassifier
        else:
            return ExtraTreesRegressor

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        if not params.get("bootstrap"):
            params.pop("max_samples")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        if self.T.goal == "class":
            criterion = ["gini", "entropy"]
        else:
            criterion = ["squared_error", "absolute_error"]

        dimensions = [
            Integer(10, 500, name="n_estimators"),
            Categorical(criterion, name="criterion"),
            Categorical([None, *list(range(1, 10))], name="max_depth"),
            Integer(2, 20, name="min_samples_split"),
            Integer(1, 20, name="min_samples_leaf"),
            Categorical([None, *np.linspace(0.5, 0.9, 5)], name="max_features"),
            Categorical([True, False], name="bootstrap"),
            Real(0, 0.035, name="ccp_alpha"),
            Categorical(np.linspace(0.5, 0.9, 5), name="max_samples"),
        ]
        return [d for d in dimensions if d.name in self.params]


class RandomForest(BaseModel):
    """Random Forest."""

    acronym = "RF"
    fullname = "Random Forest"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "n_estimators": [100, 0],
            "criterion": ["gini" if self.T.goal == "class" else "squared_error", 0],
            "max_depth": [None, 0],
            "min_samples_split": [2, 0],
            "min_samples_leaf": [1, 0],
            "max_features": [None, 0],
            "bootstrap": [False, 0],
            "ccp_alpha": [0, 3],
            "max_samples": [0.9, 1],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return RandomForestClassifier
        else:
            return RandomForestRegressor

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        if not params.get("bootstrap"):
            params.pop("max_samples")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        if self.T.goal == "class":
            criterion = ["gini", "entropy"]
        else:
            criterion = ["squared_error", "absolute_error", "poisson"]

        dimensions = [
            Integer(10, 500, name="n_estimators"),
            Categorical(criterion, name="criterion"),
            Categorical([None, *list(range(1, 10))], name="max_depth"),
            Integer(2, 20, name="min_samples_split"),
            Integer(1, 20, name="min_samples_leaf"),
            Categorical([None, *np.linspace(0.5, 0.9, 5)], name="max_features"),
            Categorical([True, False], name="bootstrap"),
            Real(0, 0.035, name="ccp_alpha"),
            Categorical(np.linspace(0.5, 0.9, 5), name="max_samples"),
        ]
        return [d for d in dimensions if d.name in self.params]


class AdaBoost(BaseModel):
    """Adaptive Boosting (with decision tree as base estimator)."""

    acronym = "AdaB"
    fullname = "AdaBoost"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {"n_estimators": [50, 0], "learning_rate": [1.0, 2]}

        # Add extra parameters depending on the task
        if self.T.goal == "class":
            self.params["algorithm"] = ["SAMME.R", 0]
        else:
            self.params["loss"] = ["linear", 0]

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return AdaBoostClassifier
        else:
            return AdaBoostRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(50, 500, name="n_estimators"),
            Real(0.01, 1.0, "log-uniform", name="learning_rate"),
            Categorical(["SAMME.R", "SAMME"], name="algorithm"),
            Categorical(["linear", "square", "exponential"], name="loss"),
        ]
        return [d for d in dimensions if d.name in self.params]


class GradientBoostingMachine(BaseModel):
    """Gradient Boosting Machine."""

    acronym = "GBM"
    fullname = "Gradient Boosting Machine"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "loss": ["deviance" if self.T.goal == "class" else "squared_error", 0],
            "learning_rate": [0.1, 2],
            "n_estimators": [100, 0],
            "subsample": [1.0, 1],
            "criterion": ["friedman_mse", 0],
            "min_samples_split": [2, 0],
            "min_samples_leaf": [1, 0],
            "max_depth": [3, 0],
            "max_features": [None, 0],
            "ccp_alpha": [0, 3],
        }

        if self.T.goal == "reg":
            self.params["alpha"] = [0.9, 1]

        # Multiclass classification only works with deviance loss
        if self.T.task.startswith("multi"):
            self.params.pop("loss")

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return GradientBoostingClassifier
        else:
            return GradientBoostingRegressor

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        if self.T.goal == "reg":
            if params.get("loss") not in ("huber", "quantile"):
                params.pop("alpha")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        if self.T.goal == "class":
            loss = ["deviance", "exponential"]  # Will never be used when multiclass
        else:
            loss = ["squared_error", "absolute_error", "huber", "quantile"]

        dimensions = [
            Categorical(loss, name="loss"),
            Real(0.01, 1.0, "log-uniform", name="learning_rate"),
            Integer(10, 500, name="n_estimators"),
            Categorical(np.linspace(0.5, 1.0, 6), name="subsample"),
            Categorical(["friedman_mse", "squared_error"], name="criterion"),
            Integer(2, 20, name="min_samples_split"),
            Integer(1, 20, name="min_samples_leaf"),
            Integer(1, 10, name="max_depth"),
            Categorical([None, *np.linspace(0.5, 0.9, 5)], name="max_features"),
            Real(0, 0.035, name="ccp_alpha"),
            Categorical(np.linspace(0.5, 0.9, 5), name="alpha"),
        ]
        return [d for d in dimensions if d.name in self.params]


class HistGBM(BaseModel):
    """Histogram-based Gradient Boosting Machine."""

    acronym = "hGBM"
    fullname = "HistGBM"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "loss": ["squared_error", 0],
            "learning_rate": [0.1, 2],
            "max_iter": [100, 0],
            "max_leaf_nodes": [31, 0],
            "max_depth": [None, 0],
            "min_samples_leaf": [20, 0],
            "l2_regularization": [0.0, 1],
        }

        if self.T.goal == "class":
            self.params.pop("loss")

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return HistGradientBoostingClassifier
        else:
            return HistGradientBoostingRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Categorical(["squared_error", "absolute_error", "poisson"], name="loss"),
            Real(0.01, 1.0, "log-uniform", name="learning_rate"),
            Integer(10, 500, name="max_iter"),
            Integer(10, 50, name="max_leaf_nodes"),
            Categorical([None, *np.linspace(1, 10, 10)], name="max_depth"),
            Integer(10, 30, name="min_samples_leaf"),
            Categorical([*np.linspace(0.0, 1.0, 11)], name="l2_regularization"),
        ]
        return [d for d in dimensions if d.name in self.params]


class XGBoost(BaseModel):
    """Extreme Gradient Boosting."""

    acronym = "XGB"
    fullname = "XGBoost"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.evals = {}
        self.params = {
            "n_estimators": [100, 0],
            "learning_rate": [0.1, 2],
            "max_depth": [6, 0],
            "gamma": [0.0, 2],
            "min_child_weight": [1, 0],
            "subsample": [1.0, 1],
            "colsample_bytree": [1.0, 1],
            "reg_alpha": [0, 0],
            "reg_lambda": [1, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        from xgboost import XGBClassifier, XGBRegressor

        if self.T.goal == "class":
            return XGBClassifier
        else:
            return XGBRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        if self.T.random_state is None:  # XGBoost can't handle random_state to be None
            random_state = params.pop("random_state", randint(0, 1e5))
        else:
            random_state = params.pop("random_state", self.T.random_state)
        return self.est_class(
            use_label_encoder=params.pop("use_label_encoder", False),
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            random_state=random_state,
            verbosity=params.pop("verbosity", 0),
            **params,
        )

    def custom_fit(self, est, train, validation=None, params=None):
        """Fit the model using early stopping and update evals attr."""
        from xgboost.callback import EarlyStopping

        params = copy(params or {})
        n_estimators = est.get_params().get("n_estimators", 100)
        rounds = self._get_early_stopping_rounds(params, n_estimators)
        eval_set = params.pop("eval_set", [train, validation] if validation else None)
        callbacks = params.pop("callbacks", [])
        if rounds:  # Add early stopping callback
            callbacks.append(EarlyStopping(rounds, maximize=True))

        est.fit(
            X=train[0],
            y=train[1],
            eval_set=eval_set,
            verbose=params.get("verbose", False),
            callbacks=callbacks,
            **params,
        )

        if validation:
            # Create evals attribute with train and validation scores
            metric_name = list(est.evals_result()["validation_0"])[0]
            self.evals = {
                "metric": metric_name,
                "train": est.evals_result()["validation_0"][metric_name],
                "test": est.evals_result()["validation_1"][metric_name],
            }
            self._stopped = (len(self.evals["train"]), n_estimators)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(20, 500, name="n_estimators"),
            Real(0.01, 1.0, "log-uniform", name="learning_rate"),
            Integer(1, 10, name="max_depth"),
            Real(0, 1.0, name="gamma"),
            Integer(1, 20, name="min_child_weight"),
            Categorical(np.linspace(0.5, 1.0, 6), name="subsample"),
            Categorical(np.linspace(0.3, 1.0, 8), name="colsample_bytree"),
            Categorical([0, 0.01, 0.1, 1, 10, 100], name="reg_alpha"),
            Categorical([0, 0.01, 0.1, 1, 10, 100], name="reg_lambda"),
        ]
        return [d for d in dimensions if d.name in self.params]


class LightGBM(BaseModel):
    """Light Gradient Boosting Machine."""

    acronym = "LGB"
    fullname = "LightGBM"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.evals = {}
        self.params = {
            "n_estimators": [100, 0],
            "learning_rate": [0.1, 2],
            "max_depth": [-1, 0],
            "num_leaves": [31, 0],
            "min_child_weight": [1, 0],
            "min_child_samples": [20, 0],
            "subsample": [1.0, 1],
            "colsample_bytree": [1.0, 1],
            "reg_alpha": [0, 0],
            "reg_lambda": [0, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        from lightgbm.sklearn import LGBMClassifier, LGBMRegressor

        if self.T.goal == "class":
            return LGBMClassifier
        else:
            return LGBMRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def custom_fit(self, est, train, validation=None, params=None):
        """Fit the model using early stopping and update evals attr."""
        from lightgbm.callback import early_stopping, log_evaluation

        params = copy(params or {})
        n_estimators = est.get_params().get("n_estimators", 100)
        rounds = self._get_early_stopping_rounds(params, n_estimators)
        eval_set = params.pop("eval_set", [train, validation] if validation else None)
        callbacks = params.pop("callbacks", [log_evaluation(0)])
        if rounds:  # Add early stopping callback
            callbacks.append(early_stopping(rounds, True, False))

        est.fit(
            X=train[0],
            y=train[1],
            eval_set=eval_set,
            callbacks=callbacks,
            **params,
        )

        if validation:
            # Create evals attribute with train and validation scores
            metric_name = list(est.evals_result_["training"])[0]  # Get first key
            self.evals = {
                "metric": metric_name,
                "train": est.evals_result_["training"][metric_name],
                "test": est.evals_result_["valid_1"][metric_name],
            }
            self._stopped = (len(self.evals["train"]), n_estimators)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(20, 500, name="n_estimators"),
            Real(0.01, 1.0, "log-uniform", name="learning_rate"),
            Categorical([-1, *list(range(1, 10))], name="max_depth"),
            Integer(20, 40, name="num_leaves"),
            Integer(1, 20, name="min_child_weight"),
            Integer(10, 30, name="min_child_samples"),
            Categorical(np.linspace(0.5, 1.0, 6), name="subsample"),
            Categorical(np.linspace(0.3, 1.0, 8), name="colsample_bytree"),
            Categorical([0, 0.01, 0.1, 1, 10, 100], name="reg_alpha"),
            Categorical([0, 0.01, 0.1, 1, 10, 100], name="reg_lambda"),
        ]
        return [d for d in dimensions if d.name in self.params]


class CatBoost(BaseModel):
    """Categorical Boosting Machine."""

    acronym = "CatB"
    fullname = "CatBoost"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.evals = {}
        self.params = {
            "n_estimators": [100, 0],
            "learning_rate": [0.1, 2],
            "max_depth": [None, 0],
            "subsample": [1.0, 1],
            "colsample_bylevel": [1.0, 1],
            "reg_lambda": [0, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        from catboost import CatBoostClassifier, CatBoostRegressor

        if self.T.goal == "class":
            return CatBoostClassifier
        else:
            return CatBoostRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            bootstrap_type=params.pop("bootstrap_type", "Bernoulli"),  # For subsample
            train_dir=params.pop("train_dir", ""),
            allow_writing_files=params.pop("allow_writing_files", False),
            thread_count=params.pop("n_jobs", self.T.n_jobs),
            random_state=params.pop("random_state", self.T.random_state),
            verbose=params.pop("verbose", False),
            **params,
        )

    def custom_fit(self, est, train, validation=None, params=None):
        """Fit the model using early stopping and update evals attr."""
        params = copy(params or {})
        n_estimators = est.get_params().get("n_estimators", 100)
        rounds = self._get_early_stopping_rounds(params, n_estimators)

        est.fit(
            X=train[0],
            y=train[1],
            eval_set=params.pop("eval_set", validation),
            early_stopping_rounds=rounds,
            **params,
        )

        if validation:
            # Create evals attribute with train and validation scores
            metric_name = list(est.evals_result_["learn"])[0]  # Get first key
            self.evals = {
                "metric": metric_name,
                "train": est.evals_result_["learn"][metric_name],
                "test": est.evals_result_["validation"][metric_name],
            }
            self._stopped = (len(self.evals["train"]), n_estimators)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        # num_leaves and min_child_samples not available for CPU implementation
        dimensions = [
            Integer(20, 500, name="n_estimators"),
            Real(0.01, 1.0, "log-uniform", name="learning_rate"),
            Categorical([None, *list(range(1, 10))], name="max_depth"),
            Categorical(np.linspace(0.5, 1.0, 6), name="subsample"),
            Categorical(np.linspace(0.3, 1.0, 8), name="colsample_bylevel"),
            Categorical([0, 0.01, 0.1, 1, 10, 100], name="reg_lambda"),
        ]
        return [d for d in dimensions if d.name in self.params]


class LinearSVM(BaseModel):
    """Linear Support Vector Machine."""

    acronym = "lSVM"
    fullname = "Linear-SVM"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "penalty": ["l2", 0],
            "loss": ["squared_hinge", 0],
            "C": [1.0, 3],
            "dual": [True, 0],
        }

        # Different params for regression tasks
        if self.T.goal == "reg":
            self.params["loss"] = ["epsilon_insensitive", 0]
            self.params.pop("penalty")

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return LinearSVC
        else:
            return LinearSVR

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        if self.T.goal == "class":
            # l1 regularization can't be combined with hinge
            if params.get("loss") == "hinge":
                params["penalty"] = "l2"
            # l1 regularization can't be combined with squared_hinge when dual=True
            if params.get("penalty") == "l1" and params.get("loss") == "squared_hinge":
                params["dual"] = False
            # l2 regularization can't be combined with hinge when dual=False
            if params.get("penalty") == "l2" and params.get("loss") == "hinge":
                params["dual"] = True
        elif params.get("loss") == "epsilon_insensitive":
            params["dual"] = True

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        if self.T.goal == "class":
            loss = ["hinge", "squared_hinge"]
        else:
            loss = ["epsilon_insensitive", "squared_epsilon_insensitive"]

        dimensions = [
            Categorical(["l1", "l2"], name="penalty"),
            Categorical(loss, name="loss"),
            Real(1e-3, 100, "log-uniform", name="C"),
            Categorical([True, False], name="loss"),
        ]
        return [d for d in dimensions if d.name in self.params]


class KernelSVM(BaseModel):
    """Kernel (non-linear) Support Vector Machine."""

    acronym = "kSVM"
    fullname = "Kernel-SVM"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "C": [1.0, 3],
            "kernel": ["rbf", 0],
            "degree": [3, 0],
            "gamma": ["scale", 0],
            "coef0": [0, 2],
            "shrinking": [True, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return SVC
        else:
            return SVR

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        if params.get("kernel") == "poly":
            params["gamma"] = "scale"  # Crashes in combination with "auto"
        else:
            params.pop("degree")

        if params.get("kernel") != "rbf":
            params.pop("coef0")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        if self.T.goal == "class":
            return self.est_class(
                random_state=params.pop("random_state", self.T.random_state),
                **params,
            )
        else:
            return self.est_class(**params)

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Real(1e-3, 100, "log-uniform", name="C"),
            Categorical(["linear", "poly", "rbf", "sigmoid"], name="kernel"),
            Integer(2, 5, name="degree"),
            Categorical(["scale", "auto"], name="gamma"),
            Real(-1.0, 1.0, name="coef0"),
            Categorical([True, False], name="shrinking"),
        ]
        return [d for d in dimensions if d.name in self.params]


class PassiveAggressive(BaseModel):
    """Passive Aggressive."""

    acronym = "PA"
    fullname = "Passive Aggressive"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "C": [1.0, 3],
            "loss": ["hinge" if self.T.goal == "class" else "epsilon_insensitive", 0],
            "average": [False, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return PassiveAggressiveClassifier
        else:
            return PassiveAggressiveRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        if self.T.goal == "class":
            return self.est_class(
                n_jobs=params.pop("n_jobs", self.T.n_jobs),
                **params,
            )
        else:
            return self.est_class(
                random_state=params.pop("random_state", self.T.random_state),
                **params,
            )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        if self.T.goal == "class":
            loss = ["hinge", "squared_hinge"]
        else:
            loss = ["epsilon_insensitive", "squared_epsilon_insensitive"]

        dimensions = [
            Real(1e-3, 100, "log-uniform", name="C"),
            Categorical(loss, name="loss"),
            Categorical([True, False], name="average"),
        ]
        return [d for d in dimensions if d.name in self.params]


class StochasticGradientDescent(BaseModel):
    """Stochastic Gradient Descent."""

    acronym = "SGD"
    fullname = "Stochastic Gradient Descent"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "loss": ["hinge" if self.T.goal == "class" else "squared_error", 0],
            "penalty": ["l2", 0],
            "alpha": [1e-4, 4],
            "l1_ratio": [0.15, 2],
            "epsilon": [0.1, 4],
            "learning_rate": ["optimal", 0],
            "eta0": [0.01, 4],
            "power_t": [0.5, 1],
            "average": [False, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return SGDClassifier
        else:
            return SGDRegressor

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = super().get_params(x)

        if params.get("penalty") != "elasticnet":
            params.pop("l1_ratio")

        if params.get("learning_rate") == "optimal":
            params.pop("eta0")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        if self.T.goal == "class":
            return self.est_class(
                random_state=params.pop("random_state", self.T.random_state),
                n_jobs=params.pop("n_jobs", self.T.n_jobs),
                **params,
            )
        else:
            return self.est_class(
                random_state=params.pop("random_state", self.T.random_state),
                **params,
            )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        loss = [
            "hinge",
            "log",
            "modified_huber",
            "squared_hinge",
            "perceptron",
            "squared_error",
            "huber",
            "epsilon_insensitive",
            "squared_epsilon_insensitive",
        ]
        learning_rate = ["constant", "invscaling", "optimal", "adaptive"]

        dimensions = [
            Categorical(loss if self.T.goal == "class" else loss[-4:], name="loss"),
            Categorical(["none", "l1", "l2", "elasticnet"], name="penalty"),
            Real(1e-4, 1.0, "log-uniform", name="alpha"),
            Categorical(np.linspace(0.05, 0.95, 19), name="l1_ratio"),
            Real(1e-4, 1.0, "log-uniform", name="epsilon"),
            Categorical(learning_rate, name="learning_rate"),
            Real(1e-4, 1.0, "log-uniform", name="eta0"),
            Categorical(np.linspace(0.1, 0.9, 9), name="power_t"),
            Categorical([True, False], name="average"),
        ]
        return [d for d in dimensions if d.name in self.params]


class MultilayerPerceptron(BaseModel):
    """Multi-layer Perceptron."""

    acronym = "MLP"
    fullname = "Multi-layer Perceptron"
    needs_scaling = True
    goal = "both"

    def __init__(self, *args):
        super().__init__(*args)
        self.params = {
            "hidden_layer_sizes": [(100, 0, 0), 0],
            "activation": ["relu", 0],
            "solver": ["adam", 0],
            "alpha": [1e-4, 4],
            "batch_size": [200, 0],
            "learning_rate": ["constant", 0],
            "learning_rate_init": [0.001, 3],
            "power_t": [0.5, 1],
            "max_iter": [200, 0],
        }

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return MLPClassifier
        else:
            return MLPRegressor

    def get_init_values(self):
        """Custom method to return the correct hidden_layer_sizes."""
        init_values = []
        for key, value in self.params.items():
            if key == "hidden_layer_sizes":
                init_values.extend(value[0])
            else:
                init_values.append(value[0])

        return init_values

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {}
        for i, key in enumerate(self.params):
            # Add extra counter for the hidden layers
            j = 2 if "hidden_layer_sizes" in self.params else 0

            if key == "hidden_layer_sizes":
                # Set the number of neurons per layer
                n1, n2, n3 = x[i], x[i + 1], x[i + 2]
                if n2 == 0:
                    layers = (n1,)
                elif n3 == 0:
                    layers = (n1, n2)
                else:
                    layers = (n1, n2, n3)

                params["hidden_layer_sizes"] = layers

            elif self.params[key][1]:  # If it has decimals...
                params[key] = round(x[i + j], self.params[key][1])
            else:
                params[key] = x[i + j]

        if params.get("solver") != "sgd":
            params.pop("learning_rate")
            params.pop("power_t")
        else:
            params.pop("learning_rate_init")

        return params

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})
        return self.est_class(
            random_state=params.pop("random_state", self.T.random_state),
            **params,
        )

    def get_dimensions(self):
        """Return a list of the bounds for the hyperparameters."""
        dimensions = [
            Integer(10, 100, name="hidden_layer_sizes"),
            Integer(0, 100, name="hidden_layer_sizes"),
            Integer(0, 100, name="hidden_layer_sizes"),
            Categorical(["identity", "logistic", "tanh", "relu"], name="activation"),
            Categorical(["lbfgs", "sgd", "adam"], name="solver"),
            Real(1e-4, 0.1, "log-uniform", name="alpha"),
            Integer(8, 250, name="batch_size"),
            Categorical(["constant", "invscaling", "adaptive"], name="learning_rate"),
            Real(1e-3, 0.1, "log-uniform", name="learning_rate_init"),
            Categorical(np.linspace(0.1, 0.9, 9), name="power_t"),
            Integer(50, 500, name="max_iter"),
        ]
        return [d for d in dimensions if d.name in self.params]


# Ensembles ======================================================== >>

class Stacking(BaseModel):
    """Class for stacking the models in the pipeline."""

    acronym = "Stack"
    fullname = "Stacking"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self._models = kwargs.pop("models")
        self._est_params = kwargs

        if any(m.branch is not self.branch for m in self._models.values()):
            raise ValueError(
                "Invalid value for the models parameter. All "
                "models must have been fitted on the current branch."
            )

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return StackingClassifier
        else:
            return StackingRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})

        estimators = []
        for m in self._models.values():
            if m.scaler:
                name = f"pipeline_{m.name}"
                est = Pipeline([("scaler", m.scaler), (m.name, m.estimator)])
            else:
                name = m.name
                est = m.estimator

            estimators.append((name, est))

        return self.est_class(
            estimators=estimators,
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            **params,
        )


class Voting(BaseModel):
    """Soft Voting/Majority Rule voting."""

    acronym = "Vote"
    fullname = "Voting"
    needs_scaling = False
    goal = "both"

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self._models = kwargs.pop("models")
        self._est_params = kwargs

        if any(m.branch is not self.branch for m in self._models.values()):
            raise ValueError(
                "Invalid value for the models parameter. All "
                "models must have been fitted on the current branch."
            )

    @property
    def est_class(self):
        """Return the estimator's class."""
        if self.T.goal == "class":
            return VotingClassifier
        else:
            return VotingRegressor

    def get_estimator(self, params=None):
        """Return the model's estimator with unpacked parameters."""
        params = copy(params or {})

        estimators = []
        for m in self._models.values():
            if m.scaler:
                name = f"pipeline_{m.name}"
                est = Pipeline([("scaler", m.scaler), (m.name, m.estimator)])
            else:
                name = m.name
                est = m.estimator

            estimators.append((name, est))

        return self.est_class(
            estimators=estimators,
            n_jobs=params.pop("n_jobs", self.T.n_jobs),
            **params,
        )


# Variables ======================================================== >>

# List of available models
MODELS = CustomDict(
    Dummy=Dummy,
    GP=GaussianProcess,
    GNB=GaussianNaiveBayes,
    MNB=MultinomialNaiveBayes,
    BNB=BernoulliNaiveBayes,
    CatNB=CategoricalNaiveBayes,
    CNB=ComplementNaiveBayes,
    OLS=OrdinaryLeastSquares,
    Ridge=Ridge,
    Lasso=Lasso,
    EN=ElasticNet,
    BR=BayesianRidge,
    ARD=AutomaticRelevanceDetermination,
    LR=LogisticRegression,
    LDA=LinearDiscriminantAnalysis,
    QDA=QuadraticDiscriminantAnalysis,
    KNN=KNearestNeighbors,
    RNN=RadiusNearestNeighbors,
    Tree=DecisionTree,
    Bag=Bagging,
    ET=ExtraTrees,
    RF=RandomForest,
    AdaB=AdaBoost,
    GBM=GradientBoostingMachine,
    hGBM=HistGBM,
    XGB=XGBoost,
    LGB=LightGBM,
    CatB=CatBoost,
    lSVM=LinearSVM,
    kSVM=KernelSVM,
    PA=PassiveAggressive,
    SGD=StochasticGradientDescent,
    MLP=MultilayerPerceptron,
)

# List of available ensembles
ENSEMBLES = CustomDict(Stack=Stacking, Vote=Voting)

# List of all models + ensembles
MODELS_ENSEMBLES = CustomDict(**MODELS, **ENSEMBLES)
