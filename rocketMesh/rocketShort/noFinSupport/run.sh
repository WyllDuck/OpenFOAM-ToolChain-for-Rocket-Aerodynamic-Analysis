cd 850k_7L
sed -i -e 's/\r$//' All*
./Allclean
./Allrun
cd ..

cd 1.5M_15L
sed -i -e 's/\r$//' All*
./Allclean
./Allrun
cd ..

#cd 3.5M_15L
#sed -i -e 's/\r$//' All*
#./Allclean
#./Allrun
#cd ..

#cd 4.5M_13L
#sed -i -e 's/\r$//' All*
#./Allclean
#./Allrun
#cd ..
