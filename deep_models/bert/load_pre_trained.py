from torch import cuda
import torch
from deep_models.bert.bert_pretrained import BERTClass

device = 'cuda' if cuda.is_available() else 'cpu'


def setup_model(number_of_classes):
    bert_model = BERTClass(number_of_classes=number_of_classes)
    bert_model.to(device)
    return bert_model


def load_model(model_file, number_of_classes):
    model = setup_model(number_of_classes)
    model.load_state_dict(torch.load(model_file))
    model.eval()
    return model
