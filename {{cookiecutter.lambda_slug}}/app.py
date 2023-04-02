import aws_cdk as cdk

from {{ cookiecutter.safe_name }}.{{ cookiecutter.safe_name }}_stack import {{ cookiecutter.application_name }}Stack


app = cdk.App()
{{ cookiecutter.application_name }}Stack(app, "{{ cookiecutter.application_name }}Stack",)
app.synth()
