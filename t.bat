@echo off


rem python ./examples/run_simulation.py
rem python ./examples/complex_example.py

cls
@echo on
python ./examples/loggerExample.py

@REM python ./examples/versionExample.py
@REM python ./src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py --suffix dev --bump patch

@REM python ./src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py

@REM python ./version_utils.py

@REM python ./examples/setupExample.py

@REM python ./examples/encryptionExample.py


@REM update the build number after every run -- once in a while sync it with the config.ini runcounter
python ./src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py --suffix dev --bump build



@REM # Make sure your code is committed
@REM git commit -am "Prepare release v0.4.7"

@REM # Create a tag
@REM git tag v0.4.7

@REM # Push the tag to origin
@REM git push origin v0.4.7

@REM python src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py --suffix release --bump minor patch
@REM python -m build
@REM rem  rem  rem  twine upload dist/*


