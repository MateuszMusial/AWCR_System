import sys
from unittest.mock import MagicMock
import pytest

# --- Global mocking setup ---
# List of modules to mock

mock_modules_to_patch = {
    'tkinter': MagicMock(),
    'tkinter.messagebox': MagicMock(),
    'ttkbootstrap': MagicMock(),
    'ttkbootstrap.constants': MagicMock(),
    'ttkbootstrap.style': MagicMock(),
    'customtkinter': MagicMock(),
    'PIL': MagicMock(),
    'PIL.Image': MagicMock(),
    'PIL.ImageTk': MagicMock(),
    'cv2': MagicMock(),
    'ultralytics': MagicMock(),
    'ultralytics.YOLO': MagicMock(),
    'easyocr': MagicMock(),
    'matplotlib': MagicMock(),
    'matplotlib.pyplot': MagicMock(),
    'matplotlib.backends.backend_tkagg': MagicMock(),
    'dotenv': MagicMock()
}

for module_name, mock_obj in mock_modules_to_patch.items():
    sys.modules[module_name] = mock_obj

if 'ttkbootstrap' in sys.modules:
    sys.modules['ttkbootstrap'].Style = MagicMock()
if 'ultralytics' in sys.modules:
    mock_yolo_instance = MagicMock()
    sys.modules['ultralytics'].YOLO = MagicMock(return_value=mock_yolo_instance)
if 'dotenv' in sys.modules:
    sys.modules['dotenv'].load_dotenv = MagicMock()

# --- End Global mocking setup ---