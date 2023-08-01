from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List

class Publicador(ABC):
    @abstractmethod
    def attach(self, subscriptor: Subscriptor) -> None:
        pass

    @abstractmethod
    def detach(self, subscriptor: Subscriptor) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

class ConcretePublicador(Publicador):
    # Status 0 --> Pending
    _state: int = 0
    _subscriptors: List[Subscriptor] = []
    _linkEmail: str = ""
    

    def attach(self, subscriptor: Subscriptor) -> None:
        print("Publicador: Attached an subscriptor.")
        self._subscriptors.append(subscriptor)

    def detach(self, subscriptor: Subscriptor) -> None:
        print("Publicador: dettached an subscriptor.")
        self._subscriptors.remove(subscriptor)

    def notify(self) -> None:
        print("Publicador: Notifying subscriptors...")
        for subscriptor in self._subscriptors:
            subscriptor.update(self)

    def some_business_logic(self, status: int) -> None:
        # Status 0 --> Pending
        # Status 1 --> Bucket
        # Status 2 --> Mail
        self._state = status
        print(f"Publicador: State changed to: {self._state}")
        self.notify()

class Subscriptor(ABC):
    @abstractmethod
    def update(self, subject: Publicador) -> None:
        pass


class ConcreteArchiveEmail(Subscriptor):
    executor: any
    params: any
    def update(self, publisher: Publicador) -> None:
        if publisher._state == 1:
            print("ConcreteObserverA: Enviando a Bucket")
            result = self.executor(self.params)
            file_link = result[0]['file_link']
            print(result)
            print()
            if file_link:
                publisher._linkEmail = file_link


        
class ConcreteEnviarCorreo(Subscriptor):
    executor: any
    params: any
    def update(self, publisher: Publicador) -> None:
        if publisher._state == 2:
            print("ConcreteObserverB: Enviando correo")
            if(publisher._linkEmail != ""):
                print(publisher._linkEmail)
                self.params['body_mail'] = self.params['body_mail'] + ' <a href="' + publisher._linkEmail +'"> Link Bucket </a>'
                result = self.executor(self.params)
