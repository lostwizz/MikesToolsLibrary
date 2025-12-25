@echo off
set VERSION=0.0.3.00354-dev

@REM set PYTHONPATH=src
@REM python loggerExample.py

cls
@echo on

@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@REM update the build number after every run -- once in a while sync it with the version.toml
python -m MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier  --bump build
@REM python -m MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier --suffix dev --bump build
@REM python -m MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier --suffix dev --bump build minor

@REM pip install -e .

@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@REM python ./examples/versionExample.py

@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
python ./examples/loggerExample.py

@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@REM python ./examples/setupExample.py


@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@REM python ./version_utils.py


@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@REM python ./examples/encryptionExample.py






@REM # Make sure your code is committed
@REM git commit -am "Prepare release v0.4.7"

@REM # Create a tag
@REM git tag v0.4.7

@REM # Push the tag to origin
@REM git push origin v0.4.7

@REM python src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py --suffix release --bump minor patch
@REM python -m build
@REM rem  rem  rem  twine upload dist/*


