import math

from .utils import operational_taxonomic_units, BinaryFeatureVector


def jaccard(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Jaccard similarity

    Same as:
        Tanimoto coefficient
    
    Jaccard, P. (1908).
    Nouvelles recherches sur la distribution florale.
    Bull. Soc. Vaud. Sci. Nat., 44, 223-270.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / (a + b + c)


def dice(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Sørensen–Dice similarity

    Same as:
        Czkanowski similarity
        Nei-Li similarity
    
    Sorensen, T. A. (1948).
    A method of establishing groups of equal amplitude in plant sociology
    based on similarity of species content and its application to analyses
    of the vegetation on Danish commons.
    Biol. Skar., 5, 1-34.

    Dice, L. R. (1945).
    Measures of the amount of ecologic association between species.
    Ecology, 26(3), 297-302    

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return (2 * a) / (2 * a + b + c)


def czekanowski(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Czkanowski similarity

    Same as:
        Sørensen–Dice coefficient
        Nei-Li similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return (2 * a) / (2 * a + b + c)


def jaccard_3w(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """3W Jaccard similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return (3 * a) / (3 * a + b + c)


def nei_li(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Nei-Li similarity

    Same as:
        Sørensen–Dice coefficient
        Czkanowski similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return (2 * a) / (2 * a + b + c)


def sokal_sneath1(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Sokal-Sneath similarity (v1)
    
    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / (a + 2 * b + 2 * c)


def smc(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Simple Matching Coefficient (SMC) similarity
    
    Sokal, R. R. (1958).
    A statistical method for evaluating systematic relationships. 
    Univ. Kansas, Sci. Bull., 38, 1409-1438.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a + d) / (a + b + c + d)


def sokal_sneath2(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Sokal-Sneath similarity (v2)
    
    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (2 * (a + d)) / (2 * a + b + c + 2 * d)


def rogers_tanimoto(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Roges-Tanimoto similarity

    Rogers, D. J., & Tanimoto, T. T. (1960).
    A computer program for classifying plants.
    Science, 132(3434), 1115-1118.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a + d) / (a + 2 * (b + c) + d)


def faith(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Faith similarity

    Faith, D. P. (1983).
    Asymmetric binary similarity measures.
    Oecologia, 57(3), 287-290.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a + 0.5 * d) / (a + b + c + d)


def gower_legendre(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Gower-Legendre similarity

    Gower, J. C., & Legendre, P. (1986).
    Metric and Euclidean properties of dissimilarity coefficients.
    Journal of classification, 3(1), 5-48.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a + d) / (a + 0.5 * (b + c) + d)


def itersection(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Intersection similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, _, _, _ = operational_taxonomic_units(x, y)

    return a


def inner_product(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Inner product similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, _, _, d = operational_taxonomic_units(x, y)

    return a + d


def russell_rao(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Russel-Rao similarity

    Rao, C. R. (1948).
    The utilization of multiple measurements in problems of biological classification.
    Journal of the Royal Statistical Society. Series B (Methodological), 10(2), 159-203.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return a / (a + b + c + d)


def cosine(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Cosine similarity

    Same as:
        Ochiai similarity (v1)
        Otsuka similarity

    Ochiai, A. (1957).
    Zoogeographic studies on the soleoid fishes found in Japan and its neighbouring regions.
    Bulletin of Japanese Society of Scientific Fisheries, 22, 526-530.

    Otsuka, Y. (1936).
    The faunal character of the Japanese Pleistocene marine Mollusca, as evidence 
    of climate having become colder during the Pleistocene in Japan.
    Biogeograph Soc Japan, 6(16), 165-170.
    
    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / math.sqrt((a + b) * (a + c))


def ochiai1(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Ochiai similarity (v1)

    Same as:
        Cosine similarity
        Otsuka similarity
    
    Ochiai, A. (1957).
    Zoogeographic studies on the soleoid fishes found in Japan and its neighbouring regions.
    Bulletin of Japanese Society of Scientific Fisheries, 22, 526-530.
        
    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """

    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / math.sqrt((a + b) * (a + c))


def otsuka(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Otsuka similarity

    Same as:
        Cosine similarity
        Ochiai similarity (v1)
    
    Otsuka, Y. (1936).
    The faunal character of the Japanese Pleistocene marine Mollusca, as evidence 
    of climate having become colder during the Pleistocene in Japan.
    Biogeograph Soc Japan, 6(16), 165-170.
        
    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """

    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / math.pow((a + b) * (a + c), 0.5)


def ochiai2(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Ochiai similarity (v2)

    Same as:
        Sokal-Sneath similarity (v5)

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """

    a, b, c, d = operational_taxonomic_units(x, y)

    return (a * d) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def sokal_sneath5(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Sokal-Sneath similarity (v5)

    Same as:
        Ochiai similarity (v2)
    
    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a * d) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def gilbert_wells(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Gilbert-Wells similarity

    Gilbert, G. K. (1884).
    Finley's tornado predictions. American Meteorological Journal.
    A Monthly Review of Meteorology and Allied Branches of Study (1884-1896), 1(5), 166.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return math.log(a) - math.log(n) - math.log((a + b) / n) - math.log((a + c) / n)


def forbes1(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Forbesi similarity (v1)

    Forbes, S. A. (1907).
    On the local distribution of certain Illinois fishes: an essay in statistical ecology (Vol. 7).
    Illinois State Laboratory of Natural History.

    Forbes, S. A. (1925).
    Method of determining and measuring the associative relations of species.
    Science, 61(1585), 518-524.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return (n * a) / ((a + b) * (a + c))


def fossum(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Fossum similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return (n * math.pow(a - 0.5, 2)) / ((a + b) * (a + c))


def sorgenfrei(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Sorgenfrei similarity

    Sorgenfrei, T. (1958).
    Molluscan Assemblages from the Marine Middle Miocene of South Jutland and their Environments. Vol. II.
    Danmarks Geologiske Undersøgelse II. Række, 79, 356-503.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return math.pow(a, 2) / ((a + b) * (a + c))


def mountford(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Mountford similarity

    Mountford, M. D. (1962).
    An index of similarity and its application to classificatory problem.
    Progress in soil zoology"(ed. Murphy, PW), 43-50.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / (0.5 * (a * b + a * c) + b * c)


def mcconnaughey(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """McConnaughey similarity

    McConnaughey, B. H. (1964).
    The determination and analysis of plankton communities.
    Lembaga Penelitian Laut.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return (math.pow(a, 2) - b * c) / ((a + b) * (a + c))


def tarwid(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Tarwid similarity

    Tarwid, K. (1960).
    Szacowanie zbieznosci nisz ekologicznych gatunkow droga oceny prawdopodobienstwa spotykania sie ich w polowach.
    Ecol Polska B (6), 115-130.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return (n * a - (a + b) * (a + c)) / (n * a + (a + b) * (a + c))


def kulczynski2(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Kulczynski similarity (v2)

    Stanisław Kulczynśki. (1927).
    Die pflanzenassoziationen der pieninen.
    Bulletin International de l'Academie Polonaise des Sciences et des Lettres, Classe des Sciences Mathematiques et Naturelles, B (Sciences Naturelles), pages 57–203.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return ((a / 2) * (2 * a + b + c)) / ((a + b) * (a + c))


def driver_kroeber(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Driver-Kroeber similarity

    Driver, H. E., & Kroeber, A. L. (1932).
    Quantitative expression of cultural relationships (Vol. 31, No. 4).
    Berkeley: University of California Press.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return (a / 2) * ((1 / (a + b) + (1 / (a + c))))


def johnson(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Johnson similarity

    Johnson, S. C. (1967).
    Hierarchical clustering schemes.
    Psychometrika, 32(3), 241-254.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / (a + b) + a / (a + c)


def dennis(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Dennis similarity

    Dennis, S. F. (1965).
    The Construction of a Thesaurus Automatically From.
    In Statistical Association Methods for Mechanized Documentation: Symposium Proceedings (Vol. 269, p. 61).
    US Government Printing Office.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return (a * d - b * c) / math.sqrt(n * (a + b) * (a + c))


def simpson(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Simpson similarity

    Simpson, E. H. (1949).
    Measurement of diversity.
    Nature, 163(4148), 688-688.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / min(a + b, a + c)


def braun_blanquet(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Braun-Banquet similarity

    Braun-Blanquet, J. (1932).
    Plant sociology. The study of plant communities. Plant sociology.
    The study of plant communities. First ed.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / max(a + b, a + c)


def fager_mcgowan(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Fager-McGowan similarity

    Fager, E. W. (1957).
    Determination and analysis of recurrent groups.
    Ecology, 38(4), 586-595.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / math.sqrt((a + b) * (a + c)) - max(a + b, a + c) / 2


def forbes2(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Forbesi similarity (v2)

    Forbes, S. A. (1907).
    On the local distribution of certain Illinois fishes: an essay in statistical ecology (Vol. 7).
    Illinois State Laboratory of Natural History.
    
    Forbes, S. A. (1925).
    Method of determining and measuring the associative relations of species.
    Science, 61(1585), 518-524.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return (n * a - (a + b) * (a + c)) / (n * min(a + b, a + c) - (a + b) * (a + c))


def sokal_sneath4(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Sokal-Sneath similarity (v4)
    
    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a / (a + b) + a / (a + c) + d / (b + d) + d / (b + d)) / 4


def gower(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Gower similarity
    
    Gower, J. C. (1971).
    A general coefficient of similarity and some of its properties.
    Biometrics, 857-871.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a + d) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def pearson1(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Pearson Chi-Squared similarity
    
    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return (n * math.pow(a * d - b * c, 2)) / ((a + b) * (a + c) * (b + d) * (c + d))


def pearson2(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Pearson similarity (v2)
    
    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    x_2 = pearson1(x, y)

    return math.sqrt(x_2 / (n + x_2))


def pearson_phi(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Pearson Phi similarity
    
    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a * d - b * c) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def pearson3(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Pearson similarity (v3)
    
    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    p = pearson_phi(x, y)

    return math.sqrt(p / (n + p))


def pearson_heron2(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Pearson-Heron similarity (v2)
    
    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return math.cos(
        (math.pi * math.sqrt(b * c)) / (math.sqrt(a * d) + math.sqrt(b * c))
    )


def sokal_sneath3(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Sokal-Sneath similarity (v3)
    
    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a + d) / (b + c)


def cole(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Cole similarity
    
    Cole, L. C. (1957).
    The measurement of partial interspecific association.
    Ecology, 38(2), 226-233.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    if a * d >= b * c:
        return (a * d - b * c) / ((a + b) * (b + d))
    elif d >= a:
        return (a * d - b * c) / ((a + b) * (a + c))
    else:
        return (a * d - b * c) / ((b + d) * (c + d))


def stiles(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Stiles similarity
    
    Stiles, H. E. (1961).
    The association factor in information retrieval.
    Journal of the ACM (JACM), 8(2), 271-279.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return math.log10(
        (n * math.pow(abs(a * d - b * c) - (n / 2), 2))
        / (a + b)
        * (a + c)
        * (b + d)
        * (c + d)
    )


def yuleq(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Yule'q similarity
    
    Yule, G. U. (1912).
    On the methods of measuring association between two attributes.
    Journal of the Royal Statistical Society, 75(6), 579-652.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a * d - b * c) / (a * d + b * c)


def yulew(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Yule w similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (math.sqrt(a * d) - math.sqrt(b * c)) / (math.sqrt(a * d) + math.sqrt(b * c))


def kulczynski1(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Kulczynski similarity (v1)

    Stanisław Kulczynśki. (1927).
    Die pflanzenassoziationen der pieninen.
    Bulletin International de l'Academie Polonaise des Sciences et des Lettres, Classe des Sciences Mathematiques et Naturelles, B (Sciences Naturelles), pages 57–203.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / (b + c)


def tanimoto(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Tanimoto similarity
    
    Tanimoto, T. T. (1968).
    An elementary mathematical theory of classification and prediction, IBM Report (November, 1958),
    cited in: G. Salton, Automatic Information Organization and Retrieval.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y)

    return a / (a + b + c)


def disperson(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Disperson similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a * d - b * c) / math.pow(a + b + c + d, 2)


def hamann(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Hamann similarity

    Hamann, U. (1961).
    Merkmalsbestand und verwandtschaftsbeziehungen der farinosae: ein beitrag zum system der monokotyledonen.
    Willdenowia, 639-768.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return ((a + d) - (b + c)) / (a + b + c + d)


def michael(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Michael similarity

    Michael, E. L. (1920).
    Marine ecology and the coefficient of association: a plea in behalf of quantitative biology.
    Journal of Ecology, 8(1), 54-59.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return 4 * (a * d - b * c) / (math.pow(a + d, 2) + math.pow(b + c, 2))


def goodman_kruskal(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Goodman-Kruskal similarity

    Goodman, L. A., & Kruskal, W. H. (1979).
    Measures of association for cross classifications.
    Measures of association for cross classifications, 2-34.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    sigma = max(a, b) + max(c, d) + max(a, c) + max(b, d)
    sigma_ = max(a + c, b + d) + max(a + b, c + d)

    return (sigma - sigma_) / (2 * n - sigma_)


def anderberg(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Anderberg similarity

    Anderberg, M. R. (2014).
    Cluster analysis for applications: probability and mathematical statistics: a series of monographs and textbooks (Vol. 19).
    Academic press.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    sigma = max(a, b) + max(c, d) + max(a, c) + max(b, d)
    sigma_ = max(a + c, b + d) + max(a + b, c + d)

    return (sigma - sigma_) / (2 * n)


def baroni_urbani_buser1(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Baroni-Urbani similarity (v1)

    Baroni-Urbani, C., & Buser, M. W. (1976).
    Similarity of binary data.
    Systematic Zoology, 25(3), 251-259.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (math.sqrt(a * d) + a) / (math.sqrt(a * d) + a + b + c)


def baroni_urbani_buser2(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Baroni-Urbani similarity (v1)

    Baroni-Urbani, C., & Buser, M. W. (1976).
    Similarity of binary data.
    Systematic Zoology, 25(3), 251-259.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (math.sqrt(a * d) + a - (b + c)) / (math.sqrt(a * d) + a + b + c)


def peirce(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Peirce similarity

    Peirce, C. S. (1884).
    The numerical measure of the success of predictions.
    Science, (93), 453-454.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a * b + b * c) / (a * b + 2 * b * c + c * d)


def eyraud(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Eyraud similarity

    Eyraud, H. (1936).
    Les principes de la mesure des correlations.
    Ann. Univ. Lyon, III. Ser., Sect. A, 1(30-47), 111.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    n = a + b + c + d

    return (math.pow(n, 2) + (n * a - (a + b) * (a + c))) / ((a + b) * (a + c) * (b + d) * (c + d))


def tarantula(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Tarantula similarity

    Jones, J. A., & Harrold, M. J. (2005, November).
    Empirical evaluation of the tarantula automatic fault-localization technique.
    In Proceedings of the 20th IEEE/ACM international Conference on Automated software engineering (pp. 273-282).

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return (a * (c + d)) / (c * (a + b))


def ample(x: BinaryFeatureVector, y: BinaryFeatureVector) -> float:
    """Ample similarity

    Abreu, R., Zoeteweij, P., & Van Gemund, A. J. (2006, December).
    An evaluation of similarity coefficients for software fault localization.
    In 2006 12th Pacific Rim International Symposium on Dependable Computing (PRDC'06) (pp. 39-46). IEEE.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y)

    return abs((a * (c + d)) / (c * (a + b)))



    