# AWS Lambda Layer with curl

[![NPM version](https://badge.fury.io/js/cdk-lambda-layer-curl.svg)](https://badge.fury.io/js/cdk-lambda-layer-curl)
[![PyPI version](https://badge.fury.io/py/cdk-lambda-layer-curl.svg)](https://badge.fury.io/py/cdk-lambda-layer-curl)
![Release](https://github.com/neilkuan/cdk-lambda-layer-curl/workflows/Release/badge.svg)

Usage:

```python
# Example automatically generated from non-compiling source. May contain errors.
// CurlLayer bundles the curl in a lambda layer
import { CurlLayer } from 'cdk-lambda-layer-curl';

declare const fn: lambda.Function;
fn.addLayers(new CurlLayer(this, 'AwsCliLayer'));
```
