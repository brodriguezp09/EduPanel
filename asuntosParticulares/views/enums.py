from enum import Enum

class EstadoSolicitud(Enum):
    CONCEDER = "Conceder"
    CONCEDER_PRIMER = "Conceder primer permiso"
    DENEGAR = "Denegar"
    DENEGAR_15 = "Denegar 15"