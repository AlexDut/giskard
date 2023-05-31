import re
import json
import random
import pandas as pd
from pathlib import Path

from ...datasets import Dataset
from ...core.core import DatasetProcessFunctionMeta
from ...ml_worker.testing.registry.registry import get_object_uuid
from ...ml_worker.testing.registry.transformation_function import TransformationFunction


class TextTransformation(TransformationFunction):
    name: str

    def __init__(self, column):
        super().__init__(None, row_level=False, cell_level=False)
        self.column = column
        self.meta = DatasetProcessFunctionMeta(type='TRANSFORMATION')
        self.meta.uuid = get_object_uuid(self)
        self.meta.code = self.name
        self.meta.name = self.name
        self.meta.display_name = self.name
        self.meta.tags = ["pickle", "scan"]
        self.meta.doc = 'Automatically generated transformation function'

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        feature_data = data[self.column].dropna().astype(str)
        data.loc[feature_data.index, self.column] = feature_data.apply(self.make_perturbation)
        return data

    def make_perturbation(self, text: str) -> str:
        raise NotImplementedError()


class TextUppercase(TextTransformation):
    name = "Transform to uppercase"

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        feature_data = data[self.column].dropna().astype(str)
        data.loc[feature_data.index, self.column] = feature_data.str.upper()
        return data


class TextLowercase(TextTransformation):
    name = "Transform to lowercase"

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        feature_data = data[self.column].dropna().astype(str)
        data.loc[feature_data.index, self.column] = feature_data.str.lower()
        return data


class TextTitleCase(TextTransformation):
    name = "Transform to title case"

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        feature_data = data[self.column].dropna().astype(str)
        data.loc[feature_data.index, self.column] = feature_data.str.title()
        return data


class TextTypoTransformation(TextTransformation):
    name = "Add typos"

    def __init__(self, column):
        super().__init__(column)
        from .entity_swap import typos

        self._typos = typos

    def make_perturbation(self, x):
        split_text = x.split(" ")
        new_text = []
        for token in split_text:
            new_text.append(self._add_typos(token))
        return " ".join(new_text)

    def _add_typos(self, word):
        # Get the token's word and apply a perturbation with probability 0.1
        if random.random() < 0.2 and len(word) > 1:
            # Choose a perturbation type randomly
            perturbation_type = random.choice(['insert', 'delete', 'replace'])
            # Apply the perturbation
            if perturbation_type == 'insert':
                idx = random.randint(0, len(word))
                new_char = chr(random.randint(33, 126))
                word = word[:idx] + new_char + word[idx:]
                return word
            elif perturbation_type == 'delete':
                idx = random.randint(0, len(word) - 1)
                word = word[:idx] + word[idx + 1 :]
                return word
            elif perturbation_type == 'replace':
                j = random.randint(0, len(word) - 1)
                c = word[j]
                if c in self._typos:
                    replacement = random.choice(self._typos[c])
                    text_modified = word[:j] + replacement + word[j + 1 :]
                    return text_modified
        return word


class TextPunctuationRemovalTransformation(TextTransformation):
    name = "Punctuation Removal"

    _punctuation = """'・﹝꛳※；〈๚“𑙢⁑៚︵｠؉︿﹜᯿｢〈＆⸲᳀࠽＿།၍𑑛［᪨𑇝።᭞፧᪩︲⸦〜᚜᳄❳࿑⁜?፣𒑱՞⸧꘍﹏᪦❭𐽗༈৽⹍𖺚﹄︑܌⸄಄࠳⦊⸑𑪞_࠲⳺⧘꛵𑗈⸳⧼‷᛭᨟܁﹃᠁﹁𑅴＠،′֊‱፡–⦃⸸﹆༄࿚𐽘܉꧟𖬷⸛❬⹋፠﹅𑈽𐩓﹎჻⦘︘𑙦*𑗕꣸％@‼᜶⁾;〟༑〕𝪉⁗︰⦋𐡗𑻷𑁊𐬺𑻸⟨⸰·︴𐮜⟬𖬹〙⁂—⸴܊𑗎𖬻࿓⸱&꧍׃〗𑗖‶𑙧？⸕𐫲𑑏༅𑱱૰࠴﹖‗𑁍𑩁܀⸷＇𑈻𑇆𖿢‸꙳⸼־؍⁘⟧₎߷𑱂⸔﹨︶࠵﹈｡𑙂꩝⳹᥅•𐫱⁔⸀«゠𑙁𛲟⟩𐮛៘⁖⸜᱿⹈𑗓࠰⵰﹐⁕﹊⸪﹟𐩕༻𑱁៙¿។࠼⸐／𑗊〉⸻﹔𐩿꓾𑩄᙮⧚𐩗᪥⸒】＊᠃𑪜𖭄❫𑑋𑪟܍٬⁀⸙〞⸌᰼𑙃𑩅⦉꛲꧉𐩔𑙩〖"౷‖﹍⁇꧞]𑇞᚛𝪋᯼⦖𑩆፥𑅵𑁇𑜾؊!⁁﹚𞥟᪫٭᜵⁆𑇟᠉。𐫶⸫؛꣼࠸𑁌‚𑱄𑥆､〽᳓﹡꓿⸞࠺𐕯”᭛″׳᰾⹁⸶𑩃꧃︳𖩯〉𑊩𑅂﹇‘＂⸺⸉෴༏᛫︓𐽖᰻⟯᳁𑂿᳇࠶₍፦𑈹，𑗌⁉𑪢！%॰𒑰⦌𑧢⸖᭜⹒༊𑑎⳼⸟⹌.𝪇︱𑑚⁋⟅၊᪭︹꡴』𑙣⸂﹫『𑗃᳆⌈՛𑗋‒𑅁：𐬻⁎𑜽︽𑙡𑁋᪤⦕𐄀⁈⸭𑁈𖬸︻༼𐄁⸬⹄﹪⌋］࿒❰𝪊๏/⹎᐀⦔„⁛﴿𑈺〛︸﹕⟪꧋﹀﹑𑗔⸘︾⸋︼⸝՝៕)࠾་𑑝‰⦍【⁚꩞⸅꫰꫱𑿿׀－𑇅꯫᪬𖺗𑈸𐩘꥟𑙬-༎𖬺𑑌‾߸⦗⁓᥄‿⦐𒑴𑃀＃𑪛៖𑂼‑꧇𑙤〰⁌︐⦅︺»‧⟮𑅀𐄂〚᳅⦄၎𐩑𑨿𑱅︒﹉᠈𑗑꤯﹂᱾⦎𑙫❪＼༆࡞༒‛𑇈᪪᪡꫟𑠻\'·𑥄𑪡܈⟦༽⸵𐤟𐮚⳾՟⸓﹗⦑؟𖺙﹋⸎#״࠷︕︙𑂻⦏⧛⦆⳻︷၌𑗂︗꧁⸠⸈᭠𞥞꧄（{𑗗⸩⦓߹⹅𑂾⁽⸡𒑳}⹃𐎟܂｣𑇍𑇇᪠𐩖੶᨞．𐫰॥﹘꧂｛𑥅⁏꧌᠄༔⸏࿔𑗍᰽⦇܆࠻؞𑗏𖩮⸇𑱃𑪠¡﴾࿐(‴、꣏⸥᯽꙾𐽕𑜼¶᯾꛴𝪈,❩꧅⁞⸢⸾⹇𐬿𑗉⸣꛷﹣⳿⸿〝܅᛬𐩒⸍;꩟𐬼§⁐⁅﹠❵᠊꣹⁙𑩀︔𐫵𖫵։⌊⟆‵܋❴‥𑪚𐬽٫⧙﹛𐽙𑈼﹌‹❱၏꩜՚፤٪꘏࿙⟭྅）〔》𑗅⹏〃𐩐⦈܄⹂𑑍𑓆𑗐❲။᭟―᭝｝𑗒᠅𑩂᳂᠀‣⟫꧈’𑙠𑱰⸤𑗁༉❯⸨۔༇⸽⹊𐏐꛶𖺘𑁉‡:፨꡷﹙᭚｟❨꫞᪣︖꣺𐫳𐫴܇꘎𒑲᠇՜﹞𐺭《𑗇꧊›।⸗⸃⸚꣎⧽꧆𑙥᪢⁊…‽᰿꤮𐬾𑙪[࠹﹒･𑗆․𐤿⹉⸹❮༐༌‟⁃⌉⸮𐮙𑙨𑃁⸁𐬹⹀\\᳃⹆׆܃༺「𑗄࠱๛⁝⸆꡵𑇛⁍᠂᠆⦒」〘𑅃⸊꡶‐†'"""

    def make_perturbation(self, x):
        split_text = x.split(" ")
        new_text = []
        for token in split_text:
            new_text.append(self._remove_punc(token))
        return " ".join(new_text)

    def _remove_punc(self, text):
        return text.translate(str.maketrans('', '', self._punctuation))


class TextLanguageBasedTransformation(TextTransformation):
    needs_dataset = True

    def __init__(self, column):
        super().__init__(column)
        self._lang_dictionary = dict()
        self._load_dictionaries()

    def _load_dictionaries(self):
        raise NotImplementedError()

    def execute(self, dataset: Dataset) -> pd.DataFrame:
        feature_data = dataset.df.loc[:, (self.column,)].dropna().astype(str)
        meta_dataframe = dataset.column_meta[self.column, "text"].add_suffix('__gsk__meta')
        feature_data = feature_data.join(meta_dataframe)
        dataset.df.loc[feature_data.index, self.column] = feature_data.apply(self.make_perturbation, axis=1)
        return dataset.df

    def make_perturbation(self, row):
        raise NotImplementedError()

    def _switch(self, word, language):
        raise NotImplementedError()

    def _select_dict(self, language):
        try:
            return self._lang_dictionary[language]
        except KeyError:
            return None


class TextGenderTransformation(TextLanguageBasedTransformation):
    name = "Switch Gender"

    def _load_dictionaries(self):
        from .entity_swap import gender_switch_en, gender_switch_fr

        self._lang_dictionary = {"en": gender_switch_en, "fr": gender_switch_fr}

    def make_perturbation(self, row):
        text = row[self.column]
        language = row["language__gsk__meta"]

        if language not in self._lang_dictionary:
            return text

        replacements = [self._switch(token, language) for token in text.split()]
        replacements = [r for r in replacements if r is not None]

        new_text = text
        for original_word, switched_word in replacements:
            new_text = re.sub(fr"\b{original_word}\b", switched_word, new_text)

        return new_text

    def _switch(self, word, language):
        try:
            return (word, self._lang_dictionary[language][word.lower()])
        except KeyError:
            return None


class TextReligionTransformation(TextLanguageBasedTransformation):
    name = "Switch Religion"

    def _load_dictionaries(self):
        from .entity_swap import religion_dict_en, religion_dict_fr

        self._lang_dictionary = {"en": religion_dict_en, "fr": religion_dict_fr}

    def make_perturbation(self, row):
        # Get text
        text = row[self.column]
        new_text = text

        # Get language and corresponding dictionary
        language = row["language__gsk__meta"]
        religion_dict = self._select_dict(language)

        # Check if we support this language
        if religion_dict is None:
            return new_text

        for religious_word_list in religion_dict:
            for i, religious_word in enumerate(religious_word_list):
                match = self._search_for_word_with_plural(word=religious_word, target_text=text)
                if match is None:
                    continue
                replacement_word = religious_word_list[(i + 1) % len(religious_word_list)]
                if replacement_word is not None:
                    lwbound, upbound = match.span()
                    new_text = (
                        new_text[:lwbound]
                        + religious_word_list[(i + 1) % len(religious_word_list)]
                        + new_text[upbound:]
                    )

        return new_text

    def _search_for_word_with_plural(self, word, target_text):
        return re.search(fr'\b{word}s?\b', target_text.lower(), re.IGNORECASE)


class TextNationalityTransformation(TextLanguageBasedTransformation):
    name = "Switch nationality"

    def _load_dictionaries(self):
        with Path(__file__).parent.joinpath("nationalities.json").open("r") as f:
            nationalities_dict = json.load(f)
        self._lang_dictionary = {"en": nationalities_dict["en"], "fr": nationalities_dict["fr"]}

    def make_perturbation(self, row):
        text = row[self.column]
        new_text = text
        language = row["language__gsk__meta"]
        nationalities_word_dict = self._select_dict(language)

        if nationalities_word_dict is None:
            return new_text

        # @TODO: clean up this code
        location_type_list = ["country", "nationality"]
        income_list = ["high-income", "low-income"]
        for income_id in range(len(income_list)):
            for location_type in location_type_list:
                for location in nationalities_word_dict[location_type][income_list[income_id]]:
                    match = re.search(fr'\b{location}\b', text.lower(), re.IGNORECASE)
                    if match is not None:
                        lwbound, upbound = match.span()
                        new_text = (
                            new_text[:lwbound]
                            + random.choice(nationalities_word_dict[location_type][income_list[(income_id + 1) % 2]])
                            + new_text[upbound:]
                        )

        return new_text
