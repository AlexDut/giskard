# 📦 Wrap your dataset

The Giskard dataset is a wrapper of `pandas.DataFrame`. It contains additional properties like the name of the target
column (ground truth variable), etc. This object gets passed to the Giskard model wrapper (
See [Wrap your model](#wrap-your-model)) for evaluation.

The `pandas.DataFrame` you provide should contain the raw data before prepocessing (categorical encoding, scaling,
etc.).

```python
from giskard import demo, Dataset

wrapped_dataset = Dataset(
  df=demo.titanic_df(),
  target="Survived",  # Optional but a MUST if available
  cat_columns=['Pclass', 'Sex', "SibSp", "Parch", "Embarked"] # Optional but a MUST if available. Inferred automatically if not.
  # name="titanic_dataset", # Optional
  # column_types=None # # Optional: if not provided, it is inferred automatically
)
```

* <mark style="color:red;">**`Mandatory parameters`**</mark>
  * `df`: A `pandas.DataFrame` that contains the raw data (before all the preprocessing steps) and the actual
    ground truth variable (target). `df` can contain more columns than the features of the model such as the sample_id,
    metadata, etc.

* <mark style="color:red;">**`Optional parameters`**</mark>
  * `target`: The column name in `dataset` corresponding to the actual target variable (ground truth).
  * `name`: Name of the wrapped dataset.
  * One of:
    * `cat_columns`: A list of strings representing the names of categorical columns. These are columns that are
      processed by the model with common categorical preprocessing, such as one hot encoding. It can be binary,
      numerical or textual with few unique values.
      If not provided, the columns types will be automatically inferred.
    * `column_types`: A dictionary of column names and their types (numeric, category or text) for all columns
      of `dataset`.
      If not provided, the types will be automatically inferred.
      
{% hint style="success" %}
To upload your dataset to the Giskard server, go to [Upload objects](docs/guide/upload/index.md) to the Giskard server.
{% endhint %}
