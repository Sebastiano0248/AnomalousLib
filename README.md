# TFG_GEINF (anticuat)

## Resum de la Implementació

Aquest projecte conté una implementació d'un generador de trajectòries utilitzant mètodes numèrics i estadístics. A continuació es descriuen els components principals:

### trajectoryGenerator.py

Aquest fitxer conté la classe `TrajectoryGenerator`, que s'encarrega de generar i mostrar trajectòries de moviment brownià en 2D. (intentar en un futur que siguin 3D)

#### Principals característiques:
- **Mètodes de generació**: Utilitza `numpy` o `scipy` per generar els increments de les trajectòries.
- **Paràmetres configurables**: Nombre de partícules, nombre de passos, interval de temps, sigma, temps inicial i final.
- **Visualització**: Permet mostrar les trajectòries generades utilitzant `matplotlib`, amb l'opció d'ajustar l'interval d'anotació dels temps.

#### Mètodes:
- `_generate_trajectories()`: Genera les trajectòries de les partícules.
- `mostrar()`: Mostra les trajectòries generades en un gràfic interactiu.

### config.py

Aquest fitxer conté les configuracions predeterminades utilitzades per `TrajectoryGenerator`, com el nombre de partícules, nombre de passos, interval de temps, sigma, temps inicial i final.
