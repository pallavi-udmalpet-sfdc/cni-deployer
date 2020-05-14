import os
import sys
import subprocess
import yaml

MANIFESTS_PATH = "Manifests"
INBOUND_HELM_TEMPLATE_PATH = "Applications/cni-inbound"
OUTBOUND_HELM_TEMPLATE_PATH = "Applications/cni-outbound"
MANIFESTS_INPUT_DIRS = ["Dev", "Prod"]
HELM_TEMPLATE_OUTPUT_PATH = os.path.join(MANIFESTS_PATH, "Output")


class ManifestProcessor:
    def __init__(self):
        pass

    def form_eks_cluster_name(self, env_name, region_name, deployment_id, direction):
        return '{}-{}-{}-{}-data-plane'.format(env_name, region_name, deployment_id, direction)

    def create_output_template_dirs(self, eks_cluster_name):

        # Create Output Directory for HELM Templates
        path = os.path.join(HELM_TEMPLATE_OUTPUT_PATH, eks_cluster_name)
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            print("Creation of the template directory %s failed" % path)
            raise e

    def generate_inbound_helm_template(self, manifest_data, manifest_file, cluster_name_suffix):
        # Inbound Dataplane Template
        inbound_eks_cluster_name = self.form_eks_cluster_name(
            manifest_data['env_name'], manifest_data['region'], manifest_data['deployment_id'], cluster_name_suffix)
        self.create_output_template_dirs(inbound_eks_cluster_name)
        response = subprocess.run(['helm', 'template', INBOUND_HELM_TEMPLATE_PATH,
                                   '--values',  manifest_file, '--output-dir', os.path.join(HELM_TEMPLATE_OUTPUT_PATH, inbound_eks_cluster_name)])
        if response.returncode != 0:
            print(response)
            sys.exit('Helm template generation failed')

    def generate_outbound_helm_template(self, manifest_data, manifest_file, cluster_name_suffix):
        outbound_eks_cluster_name = self.form_eks_cluster_name(
            manifest_data['env_name'], manifest_data['region'], manifest_data['deployment_id'], cluster_name_suffix)
        self.create_output_template_dirs(outbound_eks_cluster_name)
        response = subprocess.run(['helm', 'template', OUTBOUND_HELM_TEMPLATE_PATH,
                                   '--values',  manifest_file, '--output-dir', os.path.join(HELM_TEMPLATE_OUTPUT_PATH, outbound_eks_cluster_name)])
        if response.returncode != 0:
            print(response)
            sys.exit('Helm template generation failed')

    def generate_helm_template(self, manifest_data, manifest_file):
        # Inbound Dataplane Template
        self.generate_inbound_helm_template(
            manifest_data, manifest_file, "inbound")

        # Outbound Dataplane Template
        if "outbound_vpcs_config" in manifest_data:
            outbound_vpc_cfg = manifest_data['outbound_vpcs_config']
            outbound_vpcs_count = len(outbound_vpc_cfg['vpc_cidrs'])
            for vpc_count in range(outbound_vpcs_count):
                self.generate_outbound_helm_template(
                    manifest_data, manifest_file, "outbound-" + str(vpc_count + 1))
        else:
            self.generate_outbound_helm_template(
                manifest_data, manifest_file, "outbound")

    def process_manifest_file(self, manifest_file):
        with open(manifest_file, 'r') as file:
            manifest_data = yaml.load(file, Loader=yaml.FullLoader)
            print("***Generating Helm Templates for manifest: ", manifest_file)
            self.generate_helm_template(manifest_data, manifest_file)

    def fetch_manifest_files_list(self, manifests_dir_path):
        manifest_file_list = []
        for dirname in MANIFESTS_INPUT_DIRS:
            for root, dir_names, file_names in os.walk(os.path.join(manifests_dir_path, dirname)):
                for file_name in file_names:
                    if file_name.lower().endswith('.yaml'):
                        manifest_file_list.append(
                            os.path.join(root, file_name))
        return manifest_file_list

    def process(self):
        manifest_files = self.fetch_manifest_files_list(MANIFESTS_PATH)
        for filename in manifest_files:
            self.process_manifest_file(filename)


def main():
    manifests = ManifestProcessor()
    manifests.process()


if __name__ == "__main__":
    main()
