@ECHO OFF
setlocal
REM ---------------------------------------------------------------------------------------

REM Script to setup the environment for building Roam with QGIS 2.x.
REM This script sets the base folder that is used though out the build process
REM and sets the location to Python.

REM Change %OSGEO4W_ROOT% in setenv.bat to change in the location of QGIS.

REM ---------------------------------------------------------------------------------------


for %%x in (%cmdcmdline%) do if /i "%%~x"=="/c" set DOUBLECLICKED=1

REM Change OSGeo4W_ROOT to point to your install of QGIS.

SET OSGEO4W_ROOT=C:\OSGeo4W
SET QGISNAME=qgis
SET QGIS=%OSGEO4W_ROOT%\apps\%QGISNAME%
set QGIS_PREFIX_PATH=%QGIS%

CALL %OSGEO4W_ROOT%\bin\o4w_env.bat

: Python Setup
SET PATH=%PATH%;%OSGEO4W_ROOT%\bin;%QGIS%\bin;
SET PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27
set PYTHONPATH=%~dp0;%QGIS%\python;%PYTHONPATH%
SET QGIS_DEBUG=1
SET QGIS_LOG_FILE=C:\TEMP\qgis.log
SET QGIS_DEBUG_FILE=C:\TEMP\qgis.log
python %~dp0qgis2img %*
pause