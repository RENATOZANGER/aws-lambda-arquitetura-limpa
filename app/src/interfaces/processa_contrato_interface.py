from abc import abstractmethod, ABC


class ProcessaContratoInterface(ABC):
    @abstractmethod
    def processa_contrato(self):
        pass
