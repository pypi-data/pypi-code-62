from pathlib import Path

import fire

from hypergol.name_string import NameString
from hypergol.hypergol_project import HypergolProject


def create_model(modelName, trainingClass, evaluationClass, inputClass, outputClass, *args, projectDirectory='.', dryrun=None, force=None):
    """Generates stubs for the Tensorflow model, data processing class and training script and shell script to run it from command line

    After creation the user must implement the ``process_training_batch()`` , ``process_evaluation_batch()``, ``process_input_batch()`` and ``process_output_batch`` member functions that take  ``trainingClass``, ``evaluationClass``, ``inputClass`` and ``outputClass`` respectively.

    The model must implement the ``get_loss()``, ``produce_metrics()`` and ``get_outputs()`` functions (see documentation of :class:`.BaseTensorflowModel` and the ``Tutorial`` for more detailed instructions)

    The training script is generated with example stubs that should be modified to align with the created model.

    Parameters
    ----------
    modelName : string
        Name of the model
    trainingClass : BaseData
        Datamodel class (must exist) of the Dataset that contains the training data
    evaluationClass : BaseData
        Datamodel class (must exist) that will contain the evaluation data
    inputClass : BaseData
        Datamodel class (must exist) that will be used as the input when serving the model
    outputClass : BaseData
        Datamodel class (must exist) that will be return as output when serving the model
    *args : BaseTensorflowModelBlock
        Names of blocks that will build up the model
    """
    project = HypergolProject(projectDirectory=projectDirectory, dryrun=dryrun, force=force)
    modelName = NameString(modelName)
    trainingClass = NameString(trainingClass)
    evaluationClass = NameString(evaluationClass)
    inputClass = NameString(inputClass)
    outputClass = NameString(outputClass)
    blocks = [NameString(value) for value in args]
    project.check_dependencies([trainingClass, evaluationClass, inputClass, outputClass] + blocks)

    content = project.render(
        templateName='model.py.j2',
        templateData={
            'name': modelName,
        },
        filePath=Path(projectDirectory, 'models', modelName.asFileName)
    )

    batchProcessorContent = project.render(
        templateName='batch_processor.py.j2',
        templateData={
            'name': modelName,
            'evaluationClass': evaluationClass,
            'outputClass': outputClass,
        },
        filePath=Path(projectDirectory, 'models', f'{modelName.asSnake}_batch_processor.py')
    )

    trainModelContent = project.render(
        templateName='train_model.py.j2',
        templateData={
            'modelName': modelName,
            'trainingClass': trainingClass,
            'evaluationClass': evaluationClass,
            'blockDependencies': [name for name in blocks if project.is_model_block_class(name)],
        },
        filePath=Path(projectDirectory, 'models', f'train_{modelName.asFileName}')
    )

    scriptContent = project.render_executable(
        templateName='train_model.sh.j2',
        templateData={'snakeName': modelName.asSnake},
        filePath=Path(projectDirectory, f'train_{modelName.asSnake}.sh')
    )

    serveContent = project.render(
        templateName='serve_model.py.j2',
        templateData={
            'modelName': modelName,
            'inputClass': inputClass,
            'outputClass': outputClass
        },
        filePath=Path(projectDirectory, 'models', f'serve_{modelName.asFileName}')
    )

    serveScriptContent = project.render_executable(
        templateName='serve_model.sh.j2',
        templateData={'snakeName': modelName.asSnake},
        filePath=Path(projectDirectory, f'serve_{modelName.asSnake}.sh')
    )

    return project.cli_final_message(
        creationType='Model',
        name=modelName,
        content=(content, batchProcessorContent, trainModelContent, scriptContent, serveContent, serveScriptContent)
    )


if __name__ == "__main__":
    fire.Fire(create_model)
