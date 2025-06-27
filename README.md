# Projeto BDAI

Plataforma web de gestão de música desenvolvida em Django + PostgreSQL no contexto da unidade curricular Bases de Dados e Aplicações Inteligentes (BDAI) – 2024.

---

## Sobre o projeto

O Projeto BDAI é um _full‑stack_ académico que demonstra:

* **Backend Django 5.1** – autenticação, regras de negócio e camadas de serviço.
* **Serialização DRF** – validação de formulários sem expor endpoints REST.
* **Base de dados relacional (PostgreSQL)** com **15+ tabelas** interligadas.
* **Templates HTML/CSS/JS** – interface minimalista para administradores, artistas e consumidores.

Funcionalidades de alto nível:

| Módulo | Descrição rápida |
|--------|------------------|
| Autenticação | Registo de utilizadores, sessão e _logout_ seguro |
| Administração | Criação de artistas |
| Música & Álbuns | Upload, associação de _features_ e agrupamento em álbuns |
| Playlists | Criação, reprodução e eliminação de playlists |
| Top 10 pessoal | Histórico de visualizações |
| Pesquisa global | Pesquisa por artistas, músicas, playlists e álbuns |

> Documentação complementar nos PDFs `Relatório_BDAI.pdf` (relatório) e `2024‑BD‑projectV2.pdf` (enunciado).


---

## Instalação

### Passo‑a‑passo

```bash
git clone https://github.com/lucas03miguel/projetoBDAI.git
cd projetoBDAI

# Base de dados
python manage.py migrate

# Servidor
python manage.py runserver
```
> A parte da base de dados não está aqui implementada, pelo que nao é possível testar a aplicação. Será corrigido em breve

Navegue para <http://127.0.0.1:8000/> e explore!

---

## Utilização

* **/app/login** – Início de sessão
* **/app/registo** – Criação de conta consumidor
* **/app/index** – Dashboard consolidado
* **/app/adicionar_artista** – (Só admin) inserir artistas
* **/app/adicionar_musica** – (Só artista) publicar música
* **/app/adicionar_album** – (Só artista) compilar álbum
* **/app/adicionar_playlist** – (Só consumidor) criar playlist
* **/app/top10** – (Só consumidor) ver estatísticas pessoais

---

## Estrutura de pastas

```
projetoBDAI/
├── app/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── ficheiros python
├── projeto/            # configurações settings/urls/wsgi
├── manage.py
```
