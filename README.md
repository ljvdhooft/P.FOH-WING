# P.FOH-WING

Git manier van werken:
Snapshot aangepast op WING:
- Sla de snapshot op met de juiste lagen actief
- Mount de WING
- In WING_DATA, format de snapshot
- Maak een commit van de WING_DATA repo met de changes in de commit message
- Push de commit naar main
- Op de P.FOH WING repo, pull de main branch
- git checkout dev, git merge main —no-ff
- Push naar dev
- Automation gaat draaien, hierna pullen naar dev
- git checkout main, git merge dev —no-ff
- Push naar main
- Op de WING_DATA repo, pull van main
Snapshot aangepast in VS code:
- Maak een commit op de dev branch met de changes in de commit message
- Push naar dev
- Automation gaat draaien, hierna pullen naar dev
- git checkout main, git merge dev —no-ff
- Push naar main
- Op de WING_DATA repo, pull van main
