class Observer:
    """
    Abstract base class for observers.
    Observers are objects that need to be notified of changes in a Subject.
    """
    def update_data(self, data):
        """
        This method will be called by the Subject when it notifies its observers.
        :param data: The data passed by the Subject during notification.
        """
        raise NotImplementedError("The 'update_data' method must be implemented by the Observer subclass.")


class Subject:
    """
    Abstract base class for subjects (observables).
    Subjects are objects that maintain a list of observers and notify them of changes.
    """
    def __init__(self):
        """
        Initializes an empty list of observers.
        """
        self._observers = []

    def attach(self, observer):
        """
        Attaches an observer to the Subject.
        :param observer: An instance of a class implementing the Observer interface.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Detaches an observer from the Subject.
        :param observer: The observer to detach.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, data):
        """
        Notifies all attached observers of a change.
        :param data: The data to send to all observers.
        """
        for observer in self._observers:
            observer.update_data(data)
