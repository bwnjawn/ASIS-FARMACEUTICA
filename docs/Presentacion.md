# Backend

## Deploy en Render

Puedes revisar el estado de los despliegues del backend aquí:

https://dashboard.render.com/web/srv-d92abvdckfvc73df3su0/deploys/dep-d92cd6p9rddc738dc9l0?r=2026-07-01%4007%3A48%3A47%7E2026-07-01%4007%3A52%3A55

### Si cambias el Backend

Debes hacer:

```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

Render detectará automáticamente los cambios, recompilará el proyecto y realizará el despliegue sin necesidad de intervención adicional.

---

# Frontend

### Si cambias el Frontend

Debes volver a compilar y desplegar manualmente desde tu terminal hacia Firebase Hosting:

```bash
pnpm run build -m pwa
firebase deploy --only hosting
```

Una vez finalizado el comando, Firebase actualizará la aplicación publicada con la nueva versión del frontend.