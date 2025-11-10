import cv2
import torch
import torchvision.transforms as T
import torchvision.models as models
import urllib.request
import argparse
import sys


def load_imagenet_labels(url: str = None):
    """
    Загружает список классов ImageNet.
    Можно указать свой url или заменить на локальный файл.
    """
    if url is None:
        url = (
            "https://raw.githubusercontent.com"
            "/pytorch/hub/master/"
            "imagenet_classes.txt")
    try:
        with urllib.request.urlopen(url) as f:
            classes = [line.decode("utf-8").strip() for line in f.readlines()]
        return classes
    except Exception as e:
        print(f"Не удалось загрузить классы ImageNet: {e}")
        sys.exit(1)


def get_device(device_str: str = None) -> torch.device:
    """
    Возвращает устройство для вычислений.
    device_str: 'cpu', 'cuda' или None (автовыбор).
    """
    if device_str is None:
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    device_str = device_str.lower()
    if device_str == "cuda" and not torch.cuda.is_available():
        print("CUDA недоступна, переключаюсь на CPU.")
        return torch.device("cpu")

    return torch.device(device_str)


def create_model(model_name: str, device: torch.device):
    """
    Создает предобученную модель по имени.
    При желании сюда можно добавить больше вариантов.
    """
    model_name = model_name.lower()

    if model_name == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    elif model_name == "resnet50":
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    else:
        print(f"Неизвестная модель '{model_name}'. Использую resnet18.")
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    model.to(device)
    model.eval()
    return model


def get_preprocess_transform():
    """
    Препроцессинг под ImageNet-модели torchvision.
    """
    return T.Compose([
        T.ToPILImage(),
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def predict_frame(
        frame_bgr,
        model,
        preprocess,
        classes,
        device: torch.device
):
    """
    Делает предсказание для одного кадра (BGR от OpenCV).
    Возвращает (label, prob).
    """
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    inp = preprocess(frame_rgb).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(inp)
        probs = torch.softmax(logits, dim=1)
        top_prob, top_idx = probs.topk(1, dim=1)

    cls_id = top_idx.item()
    label = (
        classes[cls_id] if classes and cls_id < len(classes)
        else str(cls_id)
    )
    prob = top_prob.item()
    return label, prob


def process_video(video_path: str,
                  frame_step: int,
                  model,
                  preprocess,
                  classes,
                  device: torch.device):
    """
    Читает видео, берет каждый N-й кадр и выводит топ-1 предсказание.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Не удалось открыть видео: {video_path}")
        sys.exit(1)

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_step == 0:
            label, prob = (
                predict_frame(frame, model, preprocess, classes, device)
            )
            print(f"Кадр {frame_idx}: {label} (p={prob:.3f})")

        frame_idx += 1

    cap.release()


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Классификация кадров видео с помощью предобученной CNN."
        )
    )
    parser.add_argument(
        "--video", "-v",
        required=True,
        help="Путь к входному видеофайлу"
    )
    parser.add_argument(
        "--frame-step", "-s",
        type=int,
        default=30,
        help="Брать каждый N-й кадр (по умолчанию 30)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="resnet18",
        help="Имя модели torchvision (resnet18,\
              resnet50; по умолчанию resnet18)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Устройство: cpu или cuda (по умолчанию авто)"
    )
    parser.add_argument(
        "--classes-url",
        type=str,
        default=None,
        help="URL для списка классов ImageNet (опционально)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    device = get_device(args.device)
    model = create_model(args.model, device)
    preprocess = get_preprocess_transform()
    classes = load_imagenet_labels(args.classes_url)

    process_video(
        video_path=args.video,
        frame_step=args.frame_step,
        model=model,
        preprocess=preprocess,
        classes=classes,
        device=device
    )

"""
Примеры использования:
python video_classify.py --video input.mp4
python video_classify.py --video ../data/exvid3.mp4 --frame-step 5
"""

if __name__ == "__main__":
    main()

