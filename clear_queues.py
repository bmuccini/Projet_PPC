import sysv_ipc

# Clés pour les files de messages
KEY_NORD = 1000  # Clé unique qui identifie la file de messages nord
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

def clear_queue(queue):
    """Vide entièrement la file de messages."""
    while True:
        try:
            queue.receive(block=False)  # Lire et jeter le message
        except sysv_ipc.BusyError:
            break  # 🚨 Arrêter quand la queue est vide

if __name__ == "__main__":

    queue_nord = sysv_ipc.MessageQueue(KEY_NORD, sysv_ipc.IPC_CREAT)  # sysv_ipc.IPC_CREAT : flag qui indique que la file de messages doit être créée si elle n'existe pas déjà. Sinon qu'elle est simplement ouverte
    queue_sud = sysv_ipc.MessageQueue(KEY_SUD, sysv_ipc.IPC_CREAT)  # Crée et ouvre la file de messages sud
    queue_est = sysv_ipc.MessageQueue(KEY_EST, sysv_ipc.IPC_CREAT)
    queue_ouest = sysv_ipc.MessageQueue(KEY_OUEST, sysv_ipc.IPC_CREAT)
    clear_queue(queue_nord)
    clear_queue(queue_sud)
    clear_queue(queue_est)
    clear_queue(queue_ouest)
    print("Queues cleared !")
    