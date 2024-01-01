import com.sendgrid.*;
import spark.ModelAndView;
import spark.template.mustache.MustacheTemplateEngine;

import static spark.Spark.*;

public class Main {
    private static final String SENDGRID_API_KEY = "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";

    public static void main(String[] args) {
        // Set the port number
        port(8080);

        // Handle POST request for sending email
        post("/sendEmail", (request, response) -> {
            String name = request.queryParams("name");
            String email = request.queryParams("email");
            String subject = request.queryParams("subject");
            String message = request.queryParams("message");

            sendEmail(name, email, subject, message);

            return "Email sent successfully!";
        });
    }

    private static void sendEmail(String name, String email, String subject, String message) {
        Email from = new Email(email);
        Email to = new Email("dnehd5872@naver.com");
        Content content = new Content("text/plain", "Name: " + name + "\nEmail: " + email + "\n\n" + message);
        Mail mail = new Mail(from, subject, to, content);

        SendGrid sg = new SendGrid(SENDGRID_API_KEY);
        Request request = new Request();

        try {
            request.setMethod(Method.POST);
            request.setEndpoint("mail/send");
            request.setBody(mail.build());
            Response response = sg.api(request);

            if (response.getStatusCode() >= 200 && response.getStatusCode() < 300) {
                System.out.println("Email sent successfully!");
            } else {
                System.out.println("Error sending email. Status code: " + response.getStatusCode());
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            System.out.println("Error sending email: " + ex.getMessage());
        }
    }
}
