# DEFAULT WHATSAPP ELEMENT VALUES

    # New chat and search bar
NEW_CHAT = 'span[data-icon="new-chat-outline"]'
SEARCH_BAR = '#app div._aigv._aigw._aigx div[contenteditable="true"]'
SEARCH_BAR_CLEAN_BUTTON = 'span[data-icon="x-alt"]'

    # Contacts list
CHAT_LIST = '#app div._aigv._aigw._aigx div[role="button"] div._ak8l'
    
    # Looking outside | No results found
RESULTS_SUBTITLE = '#app div._aigv._aigw._aigx span._ao3e'
OFFLINE_SUBTITLE = '#app div._aigv._aigw._aigx div.x1c436fg'
    
    # Main text inputs
MAIN_TEXT_INPUT = '#main > footer div._ak1r div[contenteditable="true"]'
MAIN_SEND_BUTTON = '#main > footer div._ak1r span[data-icon="send"]'
    
    # Clip icon - files to attach
ATTACH_PLUS_BUTTON = 'span[data-icon="plus"]'
IMG_VID_BUTTON = 'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
    
    # Text input after attaching a file
FILE_TEXT_INPUT = '#app div._aigu div._aigz div[contenteditable="true"]'
FILE_SEND_BUTTON = '#app div._aigu div._aigz span[data-icon="send"]'


# DEFAULT APP VALUES
    
    # Value used for wait.until
WAIT_TIME = 10
    # Value used to wait for synchronization
SYNC_TIME = 120

    # GUI Style
GUI_TITLE = 'Zapline - WhatsApp'
SHEET_WINDOW_TITLE = 'Editar Planilha'
GUI_THEME = 'solar'

    # Path
SHEET_PATH = 'sheet.xlsx'
ICON_PATH = 'zapline.ico'


# DEFAULT APP TEXT LANGUAGE

LABEL_MESSAGE_BOX = 'Digite a mensagem:'
BUTTON_OPEN_SHEET = 'Editar arquivo no Excel'

NO_IMAGE = 'SEM IMAGEM'
INSERT_IMAGE = 'Inserir Imagem'

LABEL_TAB_DROPDOWN = 'Escolha a aba do Excel desejada:'
DEFAULT_TAB_OPTION = 'Selecione uma aba'

LABEL_LINE_ENTRY = 'Digite a linha de início (opcional):'

SEND_CHOOSE_MODE = 'Escolha uma opção de envio:'
SEND_MESSAGE_MODE = 'Apenas Mensagem'
SEND_IMAGE_MODE = 'Apenas Imagem'
SEND_IMG_MSG_MODE = 'Mensagem + Imagem'

    # Status
STATUS_DEFAULT = 'Sincronize seu telefone:'

STATUS_SYNCING = 'Sincronizando...'
STATUS_SENDING = 'Enviando...'
STATUS_STOPPING = 'Suspendendo...'

STATUS_SYNCED = 'Sincronizado'
STATUS_DONE = 'Finalizado'
STATUS_STOP = 'Suspenso'
STATUS_ERROR = 'Interrompido'

STATUS_ESTIMATIVE_CALC = 'Calculando...'
STATUS_ESTIMATIVE_LABEL = 'Estimativa:'

SPEED = 'Tempo de Espera'
    
    # Errors
ERROR_TITLE = 'Ocorreu um erro'

DEFAULT_ERROR = 'Houve um problema no último envio'
FILE_IMAGE_ERROR = 'O arquivo não é uma imagem'
SYNC_ERROR = 'Houve um problema na sincronização'
CONNECTION_ERROR = 'Conexão instável ou inexistente'
SHEET_ERROR = 'Feche a Planilha do Excel antes de prosseguir'
NO_TAB_ERROR = 'Aba inválida. Escolha uma aba existente'

    # Buttons
BUTTON_SYNC = 'Sincronizar'
BUTTON_SEND = 'Iniciar'
BUTTON_STOP = 'Parar'

    #ToolTips
SCALE_TOOLTIP = 'Conexões ou computadores lentos podem ocasionar erros no envio. Aumente o tempo de espera entre as etapas para compensar a lentidão.\n\n Caso não tenha certeza, deixe em: "1.0s".'
N_LIN_TOOLTIP = 'Digite, da aba, o número da linha que deseja iniciar o envio. Quando em branco, a primeira linha é a padrão.\n\n Caso não tenha certeza, deixe em branco.'