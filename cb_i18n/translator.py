import re
import os
import json
import warnings

TFile = re.compile("[a-z]{2,2}-[A-Z]{2,2}\\.json")

class Translator:
    """
    The message translator
    
    Attributes
    ----------
    locale_dir: Optional[str]
        The localisation directory (absolute path)
    locale_getter: Optional[Function[str]]
        The getter for locale
    translations_loaded: bool
        Whether the translation tables are loaded
    translations: Dict[str, Dict[str, str]]
        The dictionary of locale name to translation table
    """
    def __init__(self) -> None:
        self.locale_dir = None
        self.locale_getter = (lambda: lang, False)
        self.translations_loaded = False
        self.translations = {}
    
    def set_locale_dir(self, path: str) -> None:
        """
        Sets locale directory to absolute version of ``path``
        
        Parameters
        ----------
        path: str
            The path to locale
        """
        self.locale_dir = os.path.abspath(path)
    
    def set_locale_getter(self, func, asyncronous: bool = False) -> None:
        """
        Sets locale getter to ``func``
        
        Parameters
        ----------
        func: Function[str]
            The function
        asyncronous: bool
            Whether the function should be ``await``ed when called
        """
        self.locale_getter = (func, asyncronous)
    
    def load_translations(self) -> None:
        """
        Load translations from ``locale_dir`` and set every file's content to special key to ``translations``, then set ``translations_loaded`` to ``True``
        
        Raises
        ------
        RuntimeError
            You haven't set the ``locale_dir`` yet
        """
        if not self.locale_dir:
            raise RuntimeError("Locale directory must be set before loading translations")
        
        for file in os.listdir(self.locale_dir):
            if TFile.fullmatch(file):
                with open(self.locale_dir + '/' + file, 'rb') as fp:
                    self.translations[file[:5]] = json.loads(fp.read())
        
        self.translations_loaded = True
    
    def reload_translations(self) -> None:
        """
        Clears ``translations`` and ``translations_loaded``, then calls ``load_translations()``
        """
        old = self.transaltions.copy()
        self.translations = {}
        self.translations_loaded = False
        try:
            self.load_translations()
        except Exception as exc:
            self.translations = old
            self.translations_loaded = True
            warnings.warn("Failed to reload translations, falling back to the previous one.\nCaused by {}: {}".format(exc.__class__.__name__, str(exc)))
    
    def translate(self, context, message: str) -> str:
        """
        Translates ``message`` using locale got by invoking ``locale_getter()`` with given ``context`` and tables from ``translations``
        
        Returns
        -------
        str
            The translated ``message``
        
        Raises
        ------
        RuntimeError
            Translations are not loaded
        RuntimeError
            Locale getter is not set
        RuntimeError
            Translation table for locale got by ``locale_getter`` is not set
        RuntimeError
            Translation table have no translation for given ``message``
        """
        if not self.translations_loaded:
            raise RuntimeError("Translations must be loaded before translate() call")
        
        if not self.locale_getter:
            raise RuntimeError("Locale getter must be set before translate() call")
        lc = None
        
        if self.locale_getter[1] is False:
            lc = self.locale_getter[0](context)
        else:
            try:
                self.locale_getter[0](context).__await__().send(None)
            except StopIteration as exc:
                lc = exc.value
        table = self.translations.get(lc)
        
        if not table:
            raise RuntimeError("Translation table for locale \"{}\" is not set".format(repr(lc)))
        
        localized = table.get(message)
        
        if not localized:
            localized = table.get("@__default__@")
            warnings.warn("Localisation message was not found for message \"{}\". Falling back to default".format(repr(message)))
        
        if not localized:
            raise RuntimeError("Localisation message was not found and @__default__@ message was not set")
        
        return localized

def make_translator() -> Translator:
    return Translator()
