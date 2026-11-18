package br.com.barberagenda.controller;

import org.springframework.context.annotation.Profile;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.barberagenda.seed.CargaDadosFicticios;
import br.com.barberagenda.seed.ResumoCarga;

/**
 * Restauração do ambiente entre execuções de teste (manual, seção 9.1, item 6).
 * Existe SOMENTE nos perfis dev e test; em outros perfis a rota responde 404.
 * Por apagar dados, exige perfil ADMIN (ver SecurityConfig).
 */
@RestController
@RequestMapping("/api/dev")
@Profile({"dev", "test"})
public class AmbienteTesteController {

    private final CargaDadosFicticios carga;

    public AmbienteTesteController(CargaDadosFicticios carga) {
        this.carga = carga;
    }

    @PostMapping("/reset")
    public ResumoCarga restaurarDados() {
        return carga.recarregar();
    }
}
