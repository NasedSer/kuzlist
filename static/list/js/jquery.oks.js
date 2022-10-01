var input = $('#input_file');
var textarea = $('#test_box');

function getxmltext(xml, query, el) {
    var t=$(xml).find(query)
    return t.text().trim().replace(/\s{2,}/g, ' ')
}

function get_obj_data(xml, t) {
    $('#id_cad_num').val(getxmltext(xml, t + " > object > common_data > cad_number"))

    $('#id_purpose').val(getxmltext(xml, "params > purpose > value"))
    $('#id_naim').val(getxmltext(xml, "params > name"))

    $('#id_adr_oks').val(getxmltext(xml, "readable_address" ))
    $('#id_area').val(getxmltext(xml, "params > area"))
    $('#id_floors').val(getxmltext(xml, "params > floors"))
    $('#id_cost').val(getxmltext(xml, "cost > value"))

    var t=getxmltext(xml, "right_records > right_record > right_holders > right_holder > legal_entity > entity > resident > name")
    var t2=getxmltext(xml, "right_records > right_record > right_holders > right_holder > legal_entity > entity > resident > inn")
    var t3=getxmltext(xml, "right_records > right_record > right_holders > right_holder > individual")
    if (t!="") {
        $('#id_right').val(t+'ИНН '+t2)
    }
    if (t3!="") {
        $('#id_right').val(t3)
    }


	var t=$(xml).find("room_cad_numbers > room_cad_number")
	t.each(function(){
        premis = $('input.form-control[id^=id_premises_set][type=text]');
        premis.last().val($(this).text().trim());
        $('.add-row_premises_set').click();
    });
}

function get_land_data(xml, t) {
    $('#id_cad_num_land').val(getxmltext(xml, t + " > object > common_data > cad_number"))
    $('#id_land_purpose').val(getxmltext(xml, "permitted_use_established > by_document"))
    $('#id_land_area').val(getxmltext(xml, "params > area > value"))
}

function readxml(xml) {
    var t=getxmltext(xml,"object > common_data > type > value")
    if (t=='build_record') {
        $("#id_tip_oks [value='1']").attr("selected", "selected");
        get_obj_data(xml, t)
    }
    if (t=='room_record') {
        $("#id_tip_oks [value='2']").attr("selected", "selected");
        get_obj_data(xml, t)
    }
    if (t=='construction_record') {
        $("#id_tip_oks [value='3']").attr("selected", "selected");
        get_obj_data(xml, t)
    }
    if (t=='land_record') {
        get_land_data(xml, t)
    }

}

function readfiles(files) {
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        reader = new FileReader();

        reader.onload = (function(f) {
            return function(e) {
                // Here you can use `e.target.result` or `this.result`
                // and `f.name`.
                if(f.type=="text/xml") {
                    const f1 = e.target.result;
                    filecontrol = $('input.form-control[type=file]');
                    file_new = new File([f1], f.name, {type: f.type});
                    var dt = new DataTransfer();
                    dt.items.add(file_new);
                    var file_list = dt.files;
                    filecontrol[filecontrol.length-1].files=file_list;
                    $('.add-row_files_set').click();

                    xml = $.parseXML(f1);
                    readxml(xml);
                };
            };
        })(file);

    reader.onerror = (e) => alert(e.target.error.name);
    reader.readAsText(files[i]);
  }
}

var holder = document.getElementById('holder');
holder.ondragover = function () { this.className = 'hover'; return false; };
holder.ondragend = function () { this.className = ''; return false; };
holder.ondragenter = function () { this.className = ''; return false; };
holder.ondrop = function (e) {
  this.className = '';
  e.preventDefault();
  readfiles(e.dataTransfer.files);
}

function showFile(input) {
  let files = input.files;

  readfiles(files)
}