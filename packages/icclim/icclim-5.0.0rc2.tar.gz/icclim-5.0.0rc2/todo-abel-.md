Priority:
- Compléter/récrire la doc
  - Add dev doc with 
```
Release process
---------------

1. Make sure all tests pass
2. Bump version
3. Update release_notes in doc
4. Create wheel file

`[sudo] python3 setup bdist_wheel`
5. Create source archive

`[sudo] python3 -m setup sdist`

 6. Try to upload on testpypi first

`[sudo] python3 -m twine upload --repository testpypi dist/*`

7. Install testpypi version

8. Upload to pypi for real
```
  - Faire marcher les examples
  - Ajouter un pourquoi Xclim et Icclim cohabitent toujours.
  - Documenter le découpage en années provoque des pertes de "spells" sur les indices avec consecutive.
- Ajouter des tests unitaires
- Look at weighted quantile on NP
- Upload to conda
  - Wait for 5.0.0 (no rc) before pushing to conda
  - Update to rc2 for the test fixes
- Make the icclim indices accept other input frequencies (not only daily)
- Make input easier to use
  - time_range and base_period could be string like "2000-01-01" (pandas style)
  - by default out_file should be None letting the user handle `icclim.index` output
  - Create a dask client and make transfer_limit_Mbytes default to 200 ?
  - index_name could accept `EcaIndex` values
- Calculer les pdf pour verifier qui de climpact ou v5 a raison.
- Voir comment traiter le calcul s'il y a des trous dans le dataset
- Pb memoire avec dask et bootstrap
  - Voir avec Christian si c'est ok d'imposer le client Dask dans icclim afin de limiter l'utilisation de la mémoire.
  - Voir comment configurer le nombre de threads et de workers depuis icclim
  --> On veut proposer une configuration minimale par défaut dans icclim, par exemple en forçant max_tranfert_limit_truc à 200MB
      et documenter comment l'utilisateur peut monter en charge.
  --> Il faut surtout documenter l'utilisation du client Dask dans une configuration basique locale.
- Rendre icclim intelligent pour :
  1- Savoir quels indices sont utilisables avec des données mensuelles (ou annuelles si on calcule sur l'année)
  2- En entrée, pondérer selon le nombre de jours mensuels (ou annuels) 
     upsampling avec ::resample fonctionne mais utilise énormément de mémoire et de CPU
  --> En cours sur Xclim par Pascal
- Métadonnées
- Ajouter des tests unitaires

# Add documentation

# Gérer fill_value, valid_min, valid_max, valid_range surtout pour les user_indices qui ne passe pas par xclim
 - Voir ce qui était fait sur icclim 4
 - A l'écriture, remplacer les nans par des fill_value
  --> C'est géré par xclim via `decode_cf`
# type de sortie (float/single/integer) à voir sur clix-meta ce qui est fait
 --> Il n'y a pas de règle pour l'instant, voir https://github.com/clix-meta/clix-meta/issues/56

# Metadonnées
Pour chaque indice avoir les characteristique (nom, )
Pour user indice, ajouter les metadonnées dans l'input user_indice


# Add dim in User_indice to do computation on another dim than time ?

# Add percentile interpolation method
  TODO:
   - check with different density of NaNs --> Ok
   - add unit tests  --> Ok
   - try a generalization of numpy and/or scipy --> Ok
   - add documentation --> Ok on numpy
   - try with dask array --> Ok, it performs well

  Funny results:
    - When the density of NaNs is >= 60%, scipy.mquantiles stop working and always return [NaN] instead of interpolating the 40% valid data
      calc_perc is interpolating even on this case.
    - The adjustments done to avoid handling NaNs in calc_perc improve the performance my a factor 3
    - Scipy has a weird way to handle NaNs: they are taken into account to compute virtual_index instead of being ignored like in R or np.nanpercentiles.
      This is virtually pushing the quantile on the value greater than what is actual sample is showing
      For example `mquantiles([np.NaN, 41.0, 41.0, 43.0, 43.0], prob=0.5)` give 43 instead of the expected interpolation 42
      Where `mquantiles([ 41.0, 41.0, 43.0, 43.0], prob=0.5)` give the expected 42
    - When np.percentile is called with q=100, it is equal to  np.max

    Numpy does not implement the definition 8 of Hyndman and Yanan Fan (https://www.amherst.edu/media/view/129116/original/Sample+Quantiles.pdf)
    like climdex and icclim v4 do.
    On numpy they choose to implement the method 7, we can see that ilstrated here:
        line 4115 of https://github.com/numpy/numpy/blob/main/numpy/lib/function_base.py
    They did this probably because methode 7 is the default of R for historical reason (see the doc here, just above "Details": https://www.rdocumentation.org/packages/stats/versions/3.5.0/topics/quantile)
    R code: https://github.com/wch/r-source/blob/79298c499218846d14500255efd622b5021c10ec/src/library/stats/R/quantile.R

    On climdex the Cpp code is on ::c_quantile here: https://github.com/pacificclimate/climdex.pcic/blob/master/src/zhang_running_quantile.cc
    On icclim v4 the code is in libC.c::get_percentile2

    Someone implemented all methods for numpy https://github.com/ricardoV94/stats/blob/master/percentile/percentile.py

    This is kind of a mess...
    Xclim uses np.quantiles everywhere https://github.com/Ouranosinc/xclim/issues/797#issuecomment-900520700
    Dask has it's own implementation of quantiles which seems broken https://github.com/dask/dask/issues/6566
         but it seems necessary because to compute percentiles, it needs to access all the chunks https://github.com/SciTools/iris/pull/3901#issuecomment-797527498
    On Scipy, the have a fully functional implementation, but they do a complete sort of the array which is suboptimal https://github.com/scipy/scipy/blob/v1.7.1/scipy/stats/mstats_basic.py#L2659-L2784
        However, scipy also needs a 1d or 2d array, this is not a limitiation on numpy
        They also have an implementation of Harrell-Davis method not in "the 9" which, is also distribution free like the method 8
    On Numpy they don't have all the method but they have good performances
    Additionaly, on Iris, they use both scipy.mquantiles and np.percentils depending on the user input

# Add metadata
 - variable meta: auto generate the metadata from yml/excel from github or locally

# Add error codes
