package br.com.barberagenda.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/** Atalhos de navegação para as páginas estáticas. */
@Controller
public class PaginaController {

    @GetMapping({"/admin", "/admin/"})
    public String areaAdministrativa() {
        return "redirect:/admin/index.html";
    }
}
