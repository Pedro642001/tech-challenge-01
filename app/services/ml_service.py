import joblib
import numpy as np

from app.models.book import Book


class MachineLearningService:
    MODEL_PATH = "app/data/model.pkl"

    def __init__(self):
        try:
            self.model = joblib.load(self.MODEL_PATH)
        except FileNotFoundError:
            self.model = None

    async def extract_features(self):
        books = await Book.all().values("id", "title", "price", "rating", "category__name")

        features = []
        for b in books:
            features.append(
                {
                    "title": b["title"],
                    "price": b["price"],
                    "rating": b["rating"],
                    "category": b["category__name"],
                }
            )
        return features

    async def get_training_data(self):
        data = await self.extract_features()
        X, y = [], []
        for b in data:
            X.append([b["rating"]])
            y.append(b["price"])
        return np.array(X), np.array(y)

    async def train_model(self):
        from sklearn.linear_model import LinearRegression

        X, y = await self.get_training_data()

        model = LinearRegression().fit(X, y)

        joblib.dump(model, self.MODEL_PATH)

        self.model = model

        return {"message": "Modelo treinado e salvo com sucesso."}

    def predict(self, features: dict):
        if not self.model:
            raise ValueError("Modelo não treinado.")
        X = np.array([[features["rating"]]])
        prediction = self.model.predict(X)[0]
        return {"predicted_price": round(prediction, 2)}
