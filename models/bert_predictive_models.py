from utilities.app_logger import AppLogger
from utilities.file_utils import read_json
from deep_models.bert.load_pre_trained import load_model
import os
from transformers import BertTokenizer
import torch
from torch import cuda

device = 'cuda' if cuda.is_available() else 'cpu'
logger = AppLogger.getInstance()


class PredictiveModel:
    def __init__(self, root_path):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        dept_model_path = os.path.join(root_path, "Department/Department.pt")
        prob_model_path = os.path.join(root_path, "Problem/Category.pt")
        self.dept_class = read_json(os.path.join(root_path, "Department/class.json"))
        self.prob_class = read_json(os.path.join(root_path, "Problem/class.json"))
        number_dept_classes = PredictiveModel.get_classes(self.dept_class.keys())
        number_prob_classes = PredictiveModel.get_classes(self.prob_class.keys())
        self.dept_model = load_model(dept_model_path, number_dept_classes)
        self.prob_model = load_model(prob_model_path, number_prob_classes)

    @staticmethod
    def get_classes(input_dict):
        counter = 0
        while True:
            if str(counter) in input_dict:
                counter += 1
            else:
                return counter

    def get_features(self, description):
        inputs = self.tokenizer.encode_plus(
            description, None,
            add_special_tokens=True,
            MAX_LEN=512,
            pad_to_max_length=True,
            return_token_type_ids=True,
            truncation=True
        )
        ids = torch.tensor(inputs['input_ids'], dtype=torch.long)
        mask = torch.tensor(inputs['attention_mask'], dtype=torch.long)
        token_type_ids = torch.tensor(inputs["token_type_ids"], dtype=torch.long)
        return ids.reshape(1, -1), mask.reshape(1, -1), token_type_ids.reshape(1, -1)

    def inference_predictive_models(self, description):
        ids, mask, token_type_ids = self.get_features(description)
        if torch.cuda.is_available():
            ids, mask = ids.to(device, dtype=torch.long), mask.to(device, dtype=torch.long)
            token_type_ids = token_type_ids.to(device, dtype=torch.long)
        dept_output = self.dept_model(ids, mask, token_type_ids)
        dept_index = torch.max(dept_output, axis=1)[1].item()
        prob_output = self.prob_model(ids, mask, token_type_ids)
        prob_index = torch.max(prob_output, axis=1)[1].item()
        print(dept_index, prob_index)
        logger.debug(f'Predictions Category - {self.prob_class[str(prob_index)]}')
        logger.debug(f'Predictions Department - {self.dept_class[str(dept_index)]}')
        return {
            "Category": self.prob_class[str(prob_index)],
            "Department": self.dept_class[str(dept_index)]
        }
