from hyperparameter_hunter import Environment, Real, Integer, Categorical, RandomForestOptimization, ExtraTreesOptimization
from hyperparameter_hunter import BayesianOptimization, GradientBoostedRegressionTreeOptimization, DummySearch
from hyperparameter_hunter.utils.learning_utils import get_breast_cancer_data, get_toy_classification_data

from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier


def execute():
    env = Environment(
        train_dataset=get_breast_cancer_data(),
        root_results_path='HyperparameterHunterAssets',
        target_column='diagnosis',
        metrics_map=['roc_auc_score'],
        cross_validation_type=StratifiedKFold,
        cross_validation_params=dict(n_splits=10, shuffle=True, random_state=32),
        runs=2,
        file_blacklist='ALL',
    )

    # optimizer = DummySearch(
    # optimizer = GradientBoostedRegressionTreeOptimization(
    # optimizer = RandomForestOptimization(
    # optimizer = ExtraTreesOptimization(
    optimizer = BayesianOptimization(
        iterations=100, verbose=1, dimensions=[
            Integer(name='max_depth', low=2, high=20),
            Real(name='learning_rate', low=0.0001, high=0.5),
            Categorical(name='booster', categories=['gbtree', 'gblinear', 'dart'], transform='onehot'),
        ],
        # read_experiments=True,  # FLAG: ORIGINAL
        read_experiments=False,  # FLAG: TEST

        random_state=None,  # FLAG: TEST
    )

    optimizer.set_experiment_guidelines(
        model_initializer=XGBClassifier,
        model_init_params=dict(learning_rate=0.1, n_estimators=200, subsample=0.5),
    )

    # optimizer.add_init_selection('max_depth', list(range(2, 21)))
    # optimizer.add_init_selection('booster', ['gbtree', 'gblinear', 'dart'])

    optimizer.go()

    print('')


if __name__ == '__main__':
    execute()