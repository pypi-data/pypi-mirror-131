import os

YURI_API_HOST = 'http://yuri.app.kdsec.org'
TIKA_HOST = 'http://tika.app.kdsec.org'
PADDLEOCR_HOST = 'http://paddleocr.app.kdsec.org'
PDF_CONVERTER_HOST = 'http://pdf-converter.app.kdsec.org'
FILE_CONTENT_LIMIT = 5000
RETRY_API_TIMES = int(os.environ.get('RETRY_API_TIMES', 1))
