package br.com.barberagenda.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.barberagenda.model.Servico;

public interface ServicoRepository extends JpaRepository<Servico, Long> {

    List<Servico> findByAtivoTrueOrderByNomeAsc();

    List<Servico> findAllByOrderByNomeAsc();
}
