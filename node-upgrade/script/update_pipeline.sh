aws codepipeline update-pipeline --cli-input-json file://../codeseries/cdpl/shared/shared-cfn-cdpl.json --region ap-northeast-2 --profile shared-admin
aws codepipeline update-pipeline --cli-input-json file://../codeseries/cdpl/shared/shared-lambda-cdpl.json --region ap-northeast-2 --profile shared-admin

aws codepipeline update-pipeline --cli-input-json file://../codeseries/cdpl/dev/dev-cfn-cdpl.json --region ap-northeast-2 --profile dev-admin
aws codepipeline update-pipeline --cli-input-json file://../codeseries/cdpl/dev/dev-lambda-cdpl.json --region ap-northeast-2 --profile dev-admin