for d in [1-9]*/; do

        echo "$d"

	###cut
        mkdir -p results/"$d"/cutted_distance10_new/
        python ../new_scripts/all_coarse-grained_findandcut_script.py results/$d/coarse_grained/ligandr-refe.pdb results/$d/coarse_grained/receptorr-refe.pdb>results/"$d"/cutted_distance10_new/out-refe.txt
        python ../new_scripts/all_coarse-grained_findandcut_script.py results/$d/coarse_grained/ligandr.pdb results/$d/coarse_grained/receptorr.pdb>results/"$d"/cutted_distance10_new/out-unbound.txt
        mv results/$d/coarse_grained/*bound-and-flexsep.pdb results/$d/cutted_distance10_new/
	
	
	###rest
	if ! [ -d results/$d/cutted_distance10_new/ligandr/ ]
        then
                mkdir -p results/$d/cutted_distance10_new/ligandr/
                python ../new_scripts/all_coarse-grained_adjusted-rest_script.py results/$d/cutted_distance10_new/ligandr_bound-and-flexsep.pdb >results/$d/cutted_distance10_new/rest_out-unbound.txt
                mv results/$d/cutted_distance10_new/ligandr_* results/$d/cutted_distance10_new/ligandr/
        fi

        if ! [ -d results/$d/cutted_distance10_new/ligandr-refe/ ]
        then

                mkdir -p results/$d/cutted_distance10_new/ligandr-refe/
                python ../new_scripts/all_coarse-grained_adjusted-rest_script.py results/$d/cutted_distance10_new/ligandr-refe_bound-and-flexsep.pdb >results/$d/cutted_distance10_new/rest_out-refe.txt
                mv results/$d/cutted_distance10_new/ligandr-refe_* results/$d/cutted_distance10_new/ligandr-refe/
        fi

	###attract
	bash ../new_scripts/doublechains.sh $d
        if [ -f results/$d/cutted_distance10_new/ligandr/ligandr_bound-and-flexsep.pdb ]
        then
                cd results/$d/cutted_distance10_new/ligandr/
                pdbfile=ligandr_bound-and-flexsep.pdb
                python ../../../../../new_scripts/all_attract-and-collect.py $pdbfile
                cd ../../../../
        fi

        if [ -f results/$d/cutted_distance10_new/ligandr-refe/ligandr-refe_bound-and-flexsep.pdb ]
        then
                cd results/$d/cutted_distance10_new/ligandr-refe/
                pdbfile=ligandr-refe_bound-and-flexsep.pdb
                python ../../../../../new_scripts/all_attract-and-collect.py $pdbfile
                cd ../../../../
        fi


done

