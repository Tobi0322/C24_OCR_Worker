class NoValidPreprocessingStepError(Exception):
    def __str__(self):
        return repr("Each preprocessing step should implement the abstranct class PreprocessingStep that provides an execute method")


class RabbitMQWorkerNotConfiguredError(Exception):
    def __str__(self):
        return repr("Please load the configuration for Celery before calling it.")