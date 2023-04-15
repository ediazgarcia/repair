const detalleFactura = document.getElementById("detalleFactura")
const cant = document.getElementById("cant")
const desc = document.getElementById("desc")
const pund = document.getElementById("pund")
const pnet = document.getElementById("pnet")


let arrayDetalle = [];

formDetalle.onsubmit = (e)=>{
    e.preventDefault();
    const objDetalle = {
        cantidad: cant.value,
        descripcion: desc.value,
        precioUnidad: pund.value,
        precioNeto: pnet.value,
    };
    console.log(objDetalle)
};