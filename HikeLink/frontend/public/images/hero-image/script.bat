for %%F in (*) do (    
    for %%S in (320 640 960 1600 2240 3200) do (
        magick "%%F" -resize %%Sx%%S "%%~nF-%%Spx%%~xF"
        echo Imagen redimensionada: %%~nF-%%Spx%%~xF
    )
)