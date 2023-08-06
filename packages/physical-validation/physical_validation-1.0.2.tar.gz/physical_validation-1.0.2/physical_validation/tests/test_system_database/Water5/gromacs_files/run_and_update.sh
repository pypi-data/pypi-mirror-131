cd NVT/
gmx grompp -f mdout.mdp -c ../conf.gro -p ../topol.top
gmx mdrun
for ene in potential kinetic total conserved temperature pressure; do echo $ene | gmx energy -dp -f ener.edr; egrep -v "^#" energy.xvg | egrep -v "^@" | awk '{print $2;}' > ../../flat_files/NVT/$ene.dat; done 
gmx dump -f traj.trr | egrep "^ *x\[" | awk '{print $3,$4,$5; c++;}NR==15{print"";}' | sed 's/[,}]//g' > ../../flat_files/NVT/position_trajectory.xyz
gmx dump -f traj.trr | egrep "^ *v\[" | sed 's/{/ /g' | awk '{print $3,$4,$5; c++;}NR==15{print"";}' | sed 's/[,}]//g' > ../../flat_files/NVT/velocity_trajectory.xyz
cd ..

cd NPT/
gmx grompp -f mdout.mdp -c ../conf.gro -p ../topol.top
gmx mdrun
for ene in potential kinetic total conserved temperature pressure volume; do echo $ene | gmx energy -dp -f ener.edr; egrep -v "^#" energy.xvg | egrep -v "^@" | awk '{print $2;}' > ../../flat_files/NPT/$ene.dat; done 
gmx dump -f traj.trr | egrep "^ *x\[" | awk '{print $3,$4,$5; c++;}NR==15{print"";}' | sed 's/[,}]//g' > ../../flat_files/NPT/position_trajectory.xyz
gmx dump -f traj.trr | egrep "^ *v\[" | sed 's/{/ /g' | awk '{print $3,$4,$5; c++;}NR==15{print"";}' | sed 's/[,}]//g' > ../../flat_files/NPT/velocity_trajectory.xyz
cd ..
