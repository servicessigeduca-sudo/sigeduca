///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//// Main references 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//[3] * Jones, J. W. (2019). Improved automated detection of subpixel-scale inundation—Revised dynamic surface water extent (DSWE) partial surface water tests. Remote Sensing, 11(4), 374.


/*This code is code was retrieved from 
github.com/seanyx/RivWidthCloudPaper/blob/master/RivWidthCloud_JavaScript/functions_Landsat578/functions_waterClassification_Jones2019.js

water test functions for determing DSWE

ADAPTACIÓN A LANDSAT COLECCIÓN 2:
El original usaba Landsat Colección 1 SR, guardada x 10 000, por eso los umbrales de las
pruebas 4 y 5 eran 900, 1500, 1000, 3000 y 2500. Aquí la imagen llega escalada con scaler()
(reflectancia de 0 a 1), así que esos umbrales pasan a 0.09, 0.15, 0.1, 0.3 y 0.25,
los mismos que publica el USGS para la Colección 2.
Además, las bandas negativas se llevan a 0 al inicio de Dswe(), porque normalizedDifference()
enmascara los píxeles negativos y el agua oscura de las costas quedaba sin clasificar.
*/

// water test functions for determing DSWE
var Mndwi = function(image) {
  return(image.normalizedDifference(['Green', 'Swir1']).rename('mndwi'));
};
var Mbsrv = function(image) {
  return(image.select(['Green']).add(image.select(['Red'])).rename('mbsrv'));
};
var Mbsrn = function(image) {
  return(image.select(['Nir']).add(image.select(['Swir1'])).rename('mbsrn'));
};
var Ndvi = function(image) {
  return(image.normalizedDifference(['Nir', 'Red']).rename('ndvi'));
};
var Awesh = function(image) {
  return(image
  .expression('Blue + 2.5 * Green + (-1.5) * mbsrn + (-0.25) * Swir2', {
    'Blue': image.select(['Blue']),
    'Green': image.select(['Green']),
    'mbsrn': Mbsrn(image).select(['mbsrn']),
    'Swir2': image.select(['Swir2'])
  }));
};

var Dswe = function(i) {
  // En agua oscura (mar, lagos profundos) la reflectancia escalada puede ser negativa,
  // y normalizedDifference() enmascara esos píxeles. Se usa 0 como mínimo.
  i = i.select(['Blue', 'Green', 'Red', 'Nir', 'Swir1', 'Swir2']).max(0);
  var mndwi = Mndwi(i);
  var mbsrv = Mbsrv(i);
  var mbsrn = Mbsrn(i);
  var awesh = Awesh(i);
  var swir1 = i.select(['Swir1']);
  var nir = i.select(['Nir']);
  var ndvi = Ndvi(i);
  var blue = i.select(['Blue']);
  var swir2 = i.select(['Swir2']);
  
  
  var t1 = mndwi.gt(0.124);
  var t2 = mbsrv.gt(mbsrn);
  var t3 = awesh.gt(0);
  var t4 = mndwi.gt(-0.44)
  .and(swir1.lt(0.09))   // original: 900
  .and(nir.lt(0.15))     // original: 1500
  .and(ndvi.lt(0.7));
  var t5 = mndwi.gt(-0.5)
  .and(blue.lt(0.1))     // original: 1000
  .and(swir1.lt(0.3))    // original: 3000
  .and(swir2.lt(0.1))    // original: 1000
  .and(nir.lt(0.25));    // original: 2500
  
  var t = t1.add(t2.multiply(10)).add(t3.multiply(100)).add(t4.multiply(1000)).add(t5.multiply(10000));
  
  var noWater = t.eq(0)
  .or(t.eq(1))
  .or(t.eq(10))
  .or(t.eq(100))
  .or(t.eq(1000));
  var hWater = t.eq(1111)
  .or(t.eq(10111))
  .or(t.eq(11011))
  .or(t.eq(11101))
  .or(t.eq(11110))
  .or(t.eq(11111));
  var mWater = t.eq(111)
  .or(t.eq(1011))
  .or(t.eq(1101))
  .or(t.eq(1110))
  .or(t.eq(10011))
  .or(t.eq(10101))
  .or(t.eq(10110))
  .or(t.eq(11001))
  .or(t.eq(11010))
  .or(t.eq(11100));
  var pWetland = t.eq(11000);
  var lWater = t.eq(11)
  .or(t.eq(101))
  .or(t.eq(110))
  .or(t.eq(1001))
  .or(t.eq(1010))
  .or(t.eq(1100))
  .or(t.eq(10000))
  .or(t.eq(10001))
  .or(t.eq(10010))
  .or(t.eq(10100));
  
  var iDswe = noWater.multiply(0)
  .add(hWater.multiply(1))
  .add(mWater.multiply(2))
  .add(pWetland.multiply(3))
  .add(lWater.multiply(4));
  
  return(iDswe.rename('dswe'));
};

exports.ClassifyWaterJones2019 = function(img) {
  var dswe = Dswe(img);
  var waterMask = dswe.eq(1).or(dswe.eq(2)).rename(['waterMask']);
  return(waterMask);
};
