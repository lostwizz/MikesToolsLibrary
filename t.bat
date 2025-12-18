@echo off


rem python ./examples/run_simulation.py
rem python ./examples/complex_example.py

cls
@echo on
@REM python ./examples/loggerExample.py

@REM python ./examples/versionExample.py
@REM python ./src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py --suffix dev --bump patch

@REM python ./src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py

@REM python ./version_utils.py

@REM python ./examples/setupExample.py


@REM update the build number after every run -- once in a while sync it with the config.ini runcounter
python ./src/MikesToolsLibrary/MikesVersionModifier/MikesVersionModifier.py --suffix dev --bump build