$(document).ready(function () {
          let contactForm = $('.contact-form');
          let contactFormMethod = contactForm.attr('method');
          let contactFormEndPoint = contactForm.attr('action');
          let contactFormSubmitBtn = contactForm.find("[type='submit']");
          let contactFormSubmitBtnTxt = contactFormSubmitBtn.text();
          function displaySubmitting(doSubmit) {
            if (doSubmit) {
                contactFormSubmitBtn.attr('disabled', 'true');
                contactFormSubmitBtn.html("<i class='fa fa-spin fa-spinner'></i>Sending...");
            } else {
                contactFormSubmitBtn.removeAttr('disabled');
                contactFormSubmitBtn.html(contactFormSubmitBtnTxt);
            }
          }
          contactForm.submit(function (event) {
             event.preventDefault();
             let contactFormData = contactForm.serialize();
             let thisForm = $(this);
             displaySubmitting(true);
             $.ajax({
                 method: contactFormMethod,
                 url: contactFormEndPoint,
                 data: contactFormData,
                 success: function (data) {
                     thisForm[0].reset();
                      $.alert({
                         title: 'Success !',
                         content: data.message,
                         theme: 'modern',
                     });
                      setTimeout(function () {
                       displaySubmitting(false);
                      }, 2000);
                 },
                 error: function (error) {
                     displaySubmitting(false);
                     let jsonError = error.responseJSON;
                     let msg = '';
                     $.each(jsonError, function (key, value) {
                        msg += key.charAt(0).toUpperCase() + key.slice(1) + ": " + value[0].message + "<br/>";
                     });
                     $.alert({
                         title: 'Oops !',
                         content: msg,
                         theme: 'modern',
                     });
                 }
             });
          });
        });
