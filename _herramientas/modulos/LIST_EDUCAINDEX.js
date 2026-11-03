///////////////////////////////////////////////////////////////////////////////////
// UNIVERSAL LANDSAT SPECTRAL INDICES MODULE
// Compatible with Landsat 4–9 Surface Reflectance collections
// Autor: Cristian Carrascal - Canal SIG Educa
///////////////////////////////////////////////////////////////////////////////////

// --- BASE INDEX FUNCTIONS ------------------------------------------------------

exports.MBSRV = function (image){
  return image.select(['Green']).add(image.select(['Red']))
    .rename('mbsrv').toFloat();
};

exports.MBSRN = function (image){
  return image.select(['Nir']).add(image.select(['Swir1']))
    .rename('mbsrn').toFloat();
};

exports.AWESH = function (image){
  return image.expression(
    'Blue + 2.5 * Green + (-1.5) * mbsrn + (-0.25) * Swir2', {
      'Blue': image.select(['Blue']),
      'Green': image.select(['Green']),
      'mbsrn': exports.MBSRN(image).select(['mbsrn']),
      'Swir2': image.select(['Swir2'])
    }).rename('awesh').toFloat();
};

exports.NDWI = function(image){
  return image.normalizedDifference(['Green', 'Nir'])
    .rename('ndwi').toFloat();
};

exports.MNDWI = function(image){ 
  return image.expression('(Green - Swir1) / (Green + Swir1)', {
    'Green': image.select(['Green']),
    'Swir1': image.select(['Swir1'])
  }).rename('mndwi').toFloat();
};

exports.AWEI = function (image){
  return image.expression(
    '4*(Green - Swir1) - (0.25 * Nir + 2.75 * Swir2)', {
      'Green': image.select(['Green']),
      'Swir1': image.select(['Swir1']),
      'Swir2': image.select(['Swir2']),
      'Nir':   image.select(['Nir'])
  }).rename('awei').toFloat();
}; 

exports.NDVI = function (image){
  return image.normalizedDifference(['Nir', 'Red'])
    .rename('ndvi').toFloat();
};

exports.EVI = function(image){
  return image.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
      'NIR': image.select(['Nir']),
      'RED': image.select(['Red']),
      'BLUE': image.select(['Blue'])
    }).rename('evi').toFloat();
};

exports.SAVI = function(image){
  return image.expression(
    '((NIR - RED) / (NIR + RED + 0.5)) * 1.5', {
      'NIR': image.select(['Nir']),
      'RED': image.select(['Red'])
    }).rename('savi').toFloat();
};

exports.MSAVI = function(image){
  return image.expression(
    '(2 * NIR + 1 - sqrt(pow((2 * NIR + 1), 2) - 8 * (NIR - RED))) / 2', {
      'NIR': image.select(['Nir']),
      'RED': image.select(['Red'])
    }).rename('msavi').toFloat();
};

exports.NDMI = function(image){
  return image.expression('(NIR - SWIR) / (NIR + SWIR)', {
    'NIR': image.select(['Nir']),
    'SWIR': image.select(['Swir1'])
  }).rename('ndmi').toFloat();
};

exports.NBR = function(image){
  return image.expression('(NIR - SWIR) / (NIR + SWIR)', {
    'NIR': image.select(['Nir']),
    'SWIR': image.select(['Swir2'])
  }).rename('nbr').toFloat();
};

exports.NBR2 = function(image){
  return image.expression('(SWIR1 - SWIR2) / (SWIR1 + SWIR2)', {
    'SWIR1': image.select(['Swir1']),
    'SWIR2': image.select(['Swir2'])
  }).rename('nbr2').toFloat();
};

// --- MASTER FUNCTION -----------------------------------------------------------

exports.calcAllIndices = function(image){
  var indices = [
    exports.MBSRV(image),
    exports.MBSRN(image),
    exports.AWESH(image),
    exports.NDWI(image),
    exports.MNDWI(image),
    exports.AWEI(image),
    exports.NDVI(image),
    exports.EVI(image),
    exports.SAVI(image),
    exports.MSAVI(image),
    exports.NDMI(image),
    exports.NBR(image),
    exports.NBR2(image)
  ];
  
  return ee.Image.cat(indices).toFloat();
};

///////////////////////////////////////////////////////////////////////////////////
// USO DE EJEMPLO:
// var x = require('users/sigeduca/routines:Indexes/LIST_EDUCAINDEX');
// var img = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_008058_20210115');
// var bands = img.select('SR_B.').multiply(0.0000275).add(-0.2)   // reflectancia (0 a 1)
//   .select(['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7'],
//           ['Blue','Green','Red','Nir','Swir1','Swir2']);
// var indices = x.calcAllIndices(bands);
// Map.addLayer(indices.select('ndvi'), {min:0, max:1, palette:['white','green']}, 'NDVI');
///////////////////////////////////////////////////////////////////////////////////
