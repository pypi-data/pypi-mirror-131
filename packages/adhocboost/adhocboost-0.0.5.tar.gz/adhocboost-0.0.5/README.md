# AdHocBoost
[![PyPI version](https://badge.fury.io/py/adhocboost.svg)](https://github.com/deliveryhero/adhocboost)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/deliveryhero/adhocboost)

Welcome to AdHocBoost--a model that is specialized for classification in a severely imbalanced-class scenario.

## About
Many data science problems have severely imbalanced classes (e.g. predicting fraudulent transactions, predicting
order-cancellations in food-delivery, predicting if a day in Berlin will be sunny). In these situations, predicting the
positive class is hard! This module aims to alleviate some of that.

The `AdHocBoost` model works by creating `n` sequential models. The first `n-1` models can most aptly be thought of
as dataset filtering models, i.e. each one does a good job at classifying rows as "definitely _not_ the positive class"
versus "maybe the positive class". The `nth` model only works on this filtered "maybe positive" data.

Like this, the class imbalance is alleviated at each filter-step, such that by the time the dataset is filtered for
final classification by the `nth` model, the classes are considerably more balanced.

## Run Instructions
Installation is with `pip install adhocboost`. Beyond that, `AdHocBoost` conforms to a sklearn-like API: to use
it, you simply instantiate it, and then use `.fit()`, `.predict()`, and `.predict_proba()` as you see... fit ;)
