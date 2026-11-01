# Instrucciones para Claude

## Commits firmados ("Verified" en GitHub)

Los commits hechos desde las sesiones en la nube se firman automáticamente con
la clave SSH del entorno. GitHub solo los marca como **Verified** si el
*committer* sigue siendo la identidad por defecto del entorno
(`Claude <noreply@anthropic.com>`).

- No cambies `user.name` ni `user.email` (ni con `git config` ni con `-c`).
- No desactives la firma (`commit.gpgsign`, `--no-gpg-sign`).
- Para que el commit quede a nombre del dueño del sitio, usa solo `--author`:

```sh
git commit --author="SIG EDUCA <servicessigeduca-sudo@users.noreply.github.com>" -m "..."
```

Así GitHub muestra el autor `servicessigeduca-sudo` y la insignia Verified.
Si el committer se cambia a SIG EDUCA, la firma queda como `unknown_key`
(Unverified).
