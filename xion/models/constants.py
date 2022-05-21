# Tipos de documento
TIPO_DNI = '1'
TIPO_CE = '2'
TIPO_PASAPORTE = '3'
TIPO_DIE = '4'
TIPO_SIN_DOCUMENTO = '5'

DOCUMENT_TYPE_SELECTION = [
    (TIPO_DNI, 'DNI'),
    (TIPO_CE, 'Carné de extranjería'),
    (TIPO_PASAPORTE, 'Pasaporte'),
    (TIPO_DIE, 'DI extranjero'),
    (TIPO_SIN_DOCUMENTO, 'Sin Documento')
]

# Códigos de Catálogo
FEEDBACK = 'feeback'
HDSS = 'hdss'

# Estados
DRAFT = '0'
WAITING = '1'
ACTIVE = '2'
DONE = '3'
INACTIVE = '4'

STATE_SELECTION = [
    (DRAFT, 'Borrador'),
    (WAITING, 'En espera'),
    (ACTIVE, 'Activo'),
    (DONE, 'Concluido'),
    (INACTIVE, 'Inactivo')
]
