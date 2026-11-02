# -*- mode: ruby -*-
# vi: set ft=ruby :

# ホストにインストールされた VirtualBox 付属の Guest Additions ISO を探す。
# ゲストに入れるモジュールは、動かしている VirtualBox と同じ版である必要がある。
# VBOX_MSI_INSTALL_PATH は VirtualBox のインストーラが設定することがある。
def virtualbox_guest_additions_iso
  candidates = []
  if ENV["VBOX_MSI_INSTALL_PATH"]
    candidates << File.join(ENV["VBOX_MSI_INSTALL_PATH"], "VBoxGuestAdditions.iso")
  end
  candidates << "C:/Program Files/Oracle/VirtualBox/VBoxGuestAdditions.iso"
  candidates.find { |path| File.exist?(path) }
end

Vagrant.configure("2") do |config|
  config.vm.define "flask-app" do |flask_app|
    # 以前は bento/rockylinux-9 を使っていた。これは HCP Vagrant Registry
    # （旧 Vagrant Cloud）上の box で、2026-12-31 に配信が止まる。
    # Rocky Linux 公式の VirtualBox 用 box は download.rockylinux.org に直接置いてある。
    #
    # box 名に「/」を入れると Vagrant が HCP へ更新確認しに行く。
    # rocky-9 はローカルに保存するときの名前で、レジストリ上の名前ではない。
    # 版は URL のファイル名で 9.8-20260525.0 に固定し、公開されている SHA256 で検証する。
    flask_app.vm.box = "rocky-9"
    flask_app.vm.box_url = "https://download.rockylinux.org/pub/rocky/9/images/x86_64/Rocky-9-Vagrant-Vbox-9.8-20260525.0.x86_64.vagrant.virtualbox.box"
    flask_app.vm.box_download_checksum_type = "sha256"
    flask_app.vm.box_download_checksum = "beace4853d89f5d1def29fca6eec8893564882d7db85841d3d9c287ac84fb9e4"
    flask_app.vm.hostname = "flask-app.local"
    flask_app.vm.network "private_network", ip: "192.168.33.33"

    # 公式 box の同梱 Vagrantfile は次のように共有フォルダを rsync に固定している。
    #   config.vm.synced_folder ".", "/vagrant", type: "rsync"
    # プロジェクト側で種類を書かないと、この rsync 指定が残る。
    # rsync は起動時に一度コピーするだけで、ホストで編集した内容は
    # 次の rsync まで /vagrant に現れない。fileput.sh は /vagrant を直接読むので、
    # ここでは VirtualBox の共有フォルダ（vboxsf）に戻す。
    flask_app.vm.synced_folder ".", "/vagrant", type: "virtualbox"

    flask_app.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 1
      # vboxsf による共有フォルダを使う。未設定時の既定も true だが、
      # 上の type: "virtualbox" と対になる指定として明示している。
      vb.functional_vboxsf = true
    end

    # 公式 box には Guest Additions が入っていない。vboxsf が無いと共有フォルダをマウントできない。
    # Bento の Packer（guest_tools_virtualbox.sh）は box 作成時に Guest Additions を入れ、
    # vagrant up のマウントは Vagrant に任せている。ここでは作成済みの公式 box に対し、
    # 同じ導入を初回起動時に行う。
    #
    # このトリガーは CheckGuestAdditions の直前、つまり SSH が通ったあと、
    # /vagrant をマウントする前に走る。通常の provision はマウントより後なので、ここでは使えない。
    flask_app.trigger.before :"VagrantPlugins::ProviderVirtualBox::Action::CheckGuestAdditions" do |trigger|
      trigger.info = "VirtualBox Guest Additions を確認します"
      trigger.ruby do |_env, machine|
        # 2 回目以降の起動ではモジュールが既にある。導入を繰り返さない。
        next if machine.communicate.test("modprobe vboxsf", sudo: true)

        iso = virtualbox_guest_additions_iso
        if iso.nil?
          raise "VBoxGuestAdditions.iso が見つかりません。VirtualBox のインストールを確認してください。"
        end

        machine.ui.info("VirtualBox Guest Additions をインストールします")
        machine.communicate.upload(iso, "/tmp/VBoxGuestAdditions.iso")
        # <<~'SHELL' は Ruby が中身を展開しない。\$ はゲストの sed に渡すための表記。
        machine.communicate.sudo(<<~'SHELL') do |type, data|
          set -eu
          # この box の mirrorlist は、ミラーから消えた /rocky/9.8/ を返すため dnf が 404 になる。
          # $releasever は 9 であり 9.8 ではない。vault の /rocky/9/ も /rocky/9.8/ も無かった。
          # 公式の https://dl.rockylinux.org/pub/rocky/9.8/ は残っているので、そこを直接使う。
          # VERSION_ID（9.8）をパスに埋め、mirrorlist はコメントアウトする。
          version_id=$(. /etc/os-release && printf '%s' "$VERSION_ID")
          sed -i \
            -e 's/^mirrorlist=/#mirrorlist=/' \
            -e "s|^#\\?baseurl=.*\\\$releasever/|baseurl=https://dl.rockylinux.org/pub/rocky/${version_id}/|" \
            /etc/yum.repos.d/rocky*.repo
          dnf clean all
          # Bento はパッケージ更新でカーネルを上げてから kernel-devel を入れる。
          # ここではカーネルを更新しないので、起動中の uname -r に一致する kernel-devel を指定する。
          # 入っているパッケージの並びは Bento の guest_tools_virtualbox.sh に合わせている。
          # elfutils-libelf-devel は EL9 で Guest Additions のモジュールを作るときに必要になる。
          kver=$(uname -r)
          dnf install -y perl cpp gcc make bzip2 tar elfutils-libelf-devel kernel-headers "kernel-devel-${kver}"
          mkdir -p /mnt/vboxga
          mount -o loop,ro /tmp/VBoxGuestAdditions.iso /mnt/vboxga
          # インストーラは画面ドライバが無くても非 0 で終わることがある。成否は次の modinfo で見る。
          sh /mnt/vboxga/VBoxLinuxAdditions.run --nox11 || true
          umount /mnt/vboxga
          rm -f /tmp/VBoxGuestAdditions.iso
          if ! modinfo vboxsf >/dev/null 2>&1; then
            echo "vboxsf モジュールがありません" >&2
            exit 1
          fi
          # この起動の中で続くマウントが vboxsf を使えるよう、モジュールを読み込む。
          modprobe vboxsf
        SHELL
          machine.ui.detail(data.chomp) unless data.nil? || data.strip.empty?
        end
      end
    end

    # 初期設定。SELinux の無効化は設定ファイルを書き換えるだけで、反映は再起動後。
    # README の vagrant reload がそれにあたる。
    flask_app.vm.provision "shell", inline: <<-SHELL
      sudo timedatectl set-timezone Asia/Tokyo
      sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
    SHELL
  end
end
