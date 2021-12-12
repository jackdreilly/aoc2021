from pprint import pprint
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from collections import Counter
n = 50000
features = list(str(i ** 2) for i in range(n))
scores = [sum(map(int, x)) for x in features]
counts = [{k: v / len(c) for k, v in c.items()} for c in map(Counter, features)]
label = [y < x for x, y in zip(scores, scores[1:])] + [True]
print(sum(label) / len(label))
import pandas

df = pandas.DataFrame.from_records(
    [
        {
            **{
                "".join(map(str, (i, k))): v
                for i in [-1, 0]
                for k, v in counts[i + l].items()
            },
            "score": scores[l],
            "label": label[l],
        }
        for l in range(1, len(counts))
    ]
).fillna(0)

test_size = int(n / 10)
train = df.head(n - test_size)
test = df.tail(test_size)
Xr, yr = train.drop(columns="label"), train["label"]
Xt, yt = test.drop(columns="label"), test["label"]
rf = GradientBoostingClassifier().fit(Xr, yr)
print(rf.score(Xt, yt))
pprint(
    sorted(
        dict(zip(Xr.columns, rf.feature_importances_)).items(),
        key=lambda x: x[1],
        reverse=True,
    )
)
print(df.groupby('label').label.count())
