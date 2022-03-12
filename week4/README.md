# Answers to self assesment

## For query classification:

- How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 100? To 1000?
  - With 100 and basic query cleaning - `840`
  - With 1000 and basic query cleaning - `350`
- What values did you achieve for P@1, R@3, and R@5? You should have tried at least a few different models, varying the minimum number of queries per category as well as trying different fastText parameters or query normalization. Report at least 3 of your runs.

  1. 100 everything else default - Queries cleaned
     ```
     P@1     0.436
     R@1     0.436

     P@3     0.216
     R@3     0.579

     P@5     0.136
     R@5     0.679
     ```
  2. 100 -epoch 25 -wordNgrams 2 -lr 0.5 - Queries cleaned
     ```
     P@1     0.495
     R@1     0.495

     P@3     0.225
     R@3     0.676

     P@5     0.148
     R@5     0.741
     ```
  3. 1000 -wordNgrams 2 -lr (default) - Queries cleaned
     ```
     P@1     0.555
     R@1     0.555

     P@3     0.247
     R@3     0.741

     P@5     0.16
     R@5     0.802
     ```
## For integrating query classification with search:

- Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering. Make sure to include the classifier output for those queries.

  - **Tvs** showed drastic improvement in the precision of results
    - classifier output -
        ```
        [('abcat0101001', 0.4372573792934418), ('pcmcat167300050040', 0.3066013753414154), ('cat02015', 0.07877509295940399), ('pcmcat175600050011', 0.06471794843673706), ('cat09000', 0.05251004174351692)]
        ```
    - I chose `abcat0101001` and `pcmcat167300050040` to put a filter on. With a threshold of `0.3`.
  - **Beats by dre** showed more relevant earphones at the top. Since the classifier correctly predicted earbuds category with 0.63 probability.
    - classifier output -
        ```
        [('pcmcat144700050004', 0.6351504325866699), ('pcmcat143000050007', 0.24723759293556213), ('pcmcat247400050000', 0.05136178433895111), ('pcmcat143000050011', 0.04373324289917946), ('pcmcat171900050028', 0.0046333083882927895)]
        ```
    -  Only `pcmcat144700050004` qualified as a filter significantly increasing precision.


- Given 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other reason. Again, include the classifier output for those queries.
  - For query **electronics deals** classifier predicted Movies as the top category. Moreover, all the predictions were low probability.
    ```
    [('cat02015', 0.16467688977718353), ('pcmcat190000050013', 0.06162614747881889), ('pcmcat247400050000', 0.04665745422244072), ('cat02007', 0.045933373272418976), ('pcmcat174700050005', 0.03653676435351372)]
    ```
  - For query **monitors** classifier predictions were not confident enough. See all predictions below 0.26 
      ```
      [('cat09000', 0.25821444392204285), ('pcmcat219900050000', 0.2199670821428299), ('cat02692', 0.14310958981513977), ('cat02015', 0.12842734158039093), ('pcmcat200900050014', 0.12205196171998978)]
     ```