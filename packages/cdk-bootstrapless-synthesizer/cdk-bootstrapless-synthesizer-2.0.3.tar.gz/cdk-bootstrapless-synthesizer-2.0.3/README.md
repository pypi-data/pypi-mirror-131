# cdk-bootstrapless-synthesizer

[![npm version](https://img.shields.io/npm/v/cdk-bootstrapless-synthesizer)](https://www.npmjs.com/package/cdk-bootstrapless-synthesizer)
[![PyPI](https://img.shields.io/pypi/v/cdk-bootstrapless-synthesizer)](https://pypi.org/project/cdk-bootstrapless-synthesizer)
[![npm](https://img.shields.io/npm/dw/cdk-bootstrapless-synthesizer?label=npm%20downloads)](https://www.npmjs.com/package/cdk-bootstrapless-synthesizer)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/cdk-bootstrapless-synthesizer?label=pypi%20downloads)](https://pypi.org/project/cdk-bootstrapless-synthesizer)

A bootstrapless stack synthesizer that is designated to generate templates that can be directly used by AWS CloudFormation.

Please use ^1.0.0 for cdk version 1.x.x, use ^2.0.0 for cdk version 2.x.x

## Usage

```python
# Example automatically generated from non-compiling source. May contain errors.
from cdk_bootstrapless_synthesizer import BootstraplessStackSynthesizer
```

<small>[main.ts](sample/src/main.ts)</small>

```python
# Example automatically generated from non-compiling source. May contain errors.
app = App()

MyStack(app, "my-stack-dev",
    synthesizer=BootstraplessStackSynthesizer(
        template_bucket_name="cfn-template-bucket",

        file_asset_bucket_name="file-asset-bucket-${AWS::Region}",
        file_asset_region_set=["us-west-1", "us-west-2"],
        file_asset_prefix="file-asset-prefix/latest/",

        image_asset_repository_name="your-ecr-repo-name",
        image_asset_account_id="1234567890",
        image_asset_tag_prefix="latest-",
        image_asset_region_set=["us-west-1", "us-west-2"]
    )
)

# Or by environment variables
env.BSS_TEMPLATE_BUCKET_NAME = "cfn-template-bucket"

env.BSS_FILE_ASSET_BUCKET_NAME = "file-asset-bucket-${AWS::Region}"
env.BSS_FILE_ASSET_REGION_SET = "us-west-1,us-west-2"
env.BSS_FILE_ASSET_PREFIX = "file-asset-prefix/latest/"

env.BSS_IMAGE_ASSET_REPOSITORY_NAME = "your-ecr-repo-name"
env.BSS_IMAGE_ASSET_ACCOUNT_ID = "1234567890"
env.BSS_IMAGE_ASSET_TAG_PREFIX = "latest-"
env.BSS_IMAGE_ASSET_REGION_SET = "us-west-1,us-west-2"

MyStack(app, "my-stack-dev2",
    synthesizer=BootstraplessStackSynthesizer()
)
```

<small>[main.ts](sample/src/main.ts)</small>

Synth AWS CloudFormation templates, assets and upload them

```shell
$ cdk synth
$ npx cdk-assets publish -p cdk.out/my-stack-dev.assets.json -v
```

## Sample Project

See [Sample Project](./sample/README.md)

## API Reference

See [API Reference](./API.md) for API details.
