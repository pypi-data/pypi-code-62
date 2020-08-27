import pickle
import pkg_resources


def get_model():
    """
    Gets the model to predict the avocado price
    :return:
    """
    with pkg_resources.resource_stream(__name__, "model.pkl") as model_file:
        model = pickle.load(model_file)
    return model


if __name__ == '__main__':
    curr_model = get_model()
    print(curr_model.best_params_)

