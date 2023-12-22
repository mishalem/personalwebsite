/**
 * Creates a new NFT
 * @returns none
 */
function createNFT(){
    event.preventDefault();
    // package data in a JSON object
    var description = document.getElementById("description").value;
    var token = document.getElementById("token").value;

    // Allerts user if fields are empty
    if (!description || !token) {
        alert("Please fill in both Description and Token fields.");
        return;
    }
    var data_d = {'description' : document.getElementById("description").value, 'token': document.getElementById("token").value};
    console.log('data_d', data_d);

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/process_nft",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.status === '1'){
                window.location.href = "/sellerpage";
              }
        }
    });
}

/**
 * Uploads an NFT
 * @returns none
 */
function uploadNFT(){
    event.preventDefault();
    // package data in a JSON object
    var description = document.getElementById("description").value;
    var token = document.getElementById("token").value;
    var file = document.getElementById("nft_img").files[0];
    // Allerts user if fields are empty or there is no image provided
    if (!description || !token || !file) {
        alert("Please fill in both Description and Token fields as well as provide an Image.");
        return;
    }
    
    console.log('fileInput', file);
    var data_d = {'description' : description, 'token': token, 'file': file};
    console.log('data_d', data_d);

    // Construct a FormData object and append the file
    var formData = new FormData();
    formData.append("description", description);
    formData.append("token", token);
    formData.append("file", file);


    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/upload_nft",
        data: formData,
        processData: false,
        contentType: false,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.status === '1'){
                window.location.href = "/sellerpage";
              }
              else{
                alert("Upload of an NFT failed.");
                return;
              }
        }
    });
}

/**
 * Edits NFT
 */
function editNFT() {
    // updates description of an NFT
    $('input[id^="nftDescription_"]').each(function() {
        var nft_id = $(this).attr('id').split('_')[1];
        var description = $(this).val();
        data_d = {'nft_id' : nft_id, 'description' : description};
        console.log('data_d', data_d);
                jQuery.ajax({
                url: "/update_nft_description",
                data: data_d,
                type: "POST",   
                async: false,  
                    success: function(response) {
                }
            });
        });
    // updates token of an NFT
    $('input[id^="nftToken_"]').each(function() {
        var nft_id = $(this).attr('id').split('_')[1];
        var token = $(this).val();
        data_d = {'nft_id' : nft_id, 'token' : token};
                jQuery.ajax({
                url: "/update_nft_token",
                data: data_d,
                type: "POST",   
                async: false,  
                    success: function(response) {
                }
            });
        });
}
/**
 * Proccesses buy transaction
 * @param  nft_id id of the NFT to be bought
 * @returns 
 */
function buyNFT(nft_id){
    event.preventDefault();
    // package data in a JSON object
    //var nft_id = document.getElementById("nft_id").getAttribute("value");
    var token = document.getElementById("token_nft").getAttribute("value");
    var buyer_balance = document.getElementById("user_balance").getAttribute("value");
    var buyer = document.getElementById("user").getAttribute("value");

    console.log("token", token);
    console.log("buyer_balance", buyer_balance);

    if (parseInt(token) > parseInt(buyer_balance)) {
        alert("You do not have enough tokens to buy this NFT.");
        return;
    }

    var data_d = {'nft_id' : nft_id, 'token': token, 'buyer': buyer};
    console.log('data_d', data_d);

    jQuery.ajax({
        url: "/process_transaction",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.status === '1'){
                window.location.href = "/sellerpage";
              }
        }
    });
}

/**
 * Shows all NFT's transactions
 * @param nft_id id of the nft
 */
// keeps track of transactions of what nft_id has been shown
let count = {};
function showNFT(nft_id){
    event.preventDefault();
    // package data in a JSON object
    var data_d = {'nft_id' : nft_id};
    console.log('data_d', data_d);
    jQuery.ajax({
        url: "/show_nft",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              console.log("count", count);
              if (count[nft_id] === true) {
                return;}
                for (var key in returned_data) {
                var transaction = returned_data[key];
                //Creates transaction element as a div
                var transactionElement = document.createElement('div');
                transactionElement.innerHTML = '<p>Transaction #' + key.toString() + '</p>' +
                                                '<p>Cost: ' + transaction['cost'] + '</p>' +
                                                '<p>Seller: ' + transaction['seller'] + '</p>' +
                                                '<p>Buyer: ' + transaction['buyer'] + '</p>' +
                                                '<p>Owner: ' + transaction['owner'] + '</p>' +
                                                '<p>Date: ' + transaction['date'] + '</p>' +
                                                '<p>NFT ID: ' + transaction['nft_id'] + '</p>';
                var wrapper = document.getElementsByClassName('nft_wrapper')[transaction['nft_id'] - 1];
                wrapper.appendChild(transactionElement);
            }
            if (Object.keys(returned_data).length === 0){
                alert("This NFT has not yet been involved in any transactions.");
                return; 
            }
            count[nft_id] = true;
        }
    });
}